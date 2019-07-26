import bz2
import csv
import logging
import re
from pathlib import Path
from typing import Generator, List

import mwparserfromhell as mwp
import requests
from lxml import etree
from lxml.etree import Element
from mwparserfromhell.nodes.extras import Parameter
from mwparserfromhell.nodes.template import Template
from mwparserfromhell.nodes.text import Text
from mwparserfromhell.nodes.wikilink import Wikilink
from mwparserfromhell.wikicode import Wikicode

from templates import get_template_parser

NAMESPACE = "{http://www.mediawiki.org/xml/export-0.10/}"

WIKI_FILENAME = "enwiktionary-latest-pages-articles.xml.bz2"
WIKTIONARY_URL = "https://dumps.wikimedia.your.org/enwiktionary/latest/{}".format(WIKI_FILENAME)


DOWNLOAD_PATH = Path("/tmp").joinpath(WIKI_FILENAME)
OUTPUT_DIR = Path.cwd()
ETYMOLOGY_PATH = OUTPUT_DIR.joinpath("etymology.csv")
IPA_PATH = OUTPUT_DIR.joinpath("pronunciation.csv")


def tag(s: str):
    return NAMESPACE + s


def download(url: str) -> None:
    """
    Downloads the file at the URL to `DOWNLOAD_PATH`
    """
    if DOWNLOAD_PATH.exists():
        logging.info("File already exists, skipping download.")
        return

    logging.info("Downloading {}".format(url))
    r = requests.get(url)
    with open(DOWNLOAD_PATH, 'wb') as f:
        f.write(r.content)
    logging.info("Downloaded {}".format(url))


def stream_xml() -> Element:
    with bz2.open(DOWNLOAD_PATH, "rb") as f_in, open(ETYMOLOGY_PATH, "w") as f_out:
        words = 0
        etys = 0
        writer = csv.writer(f_out)
        for event, elem in etree.iterparse(f_in, huge_tree=True):
            if elem.tag == tag("text"):
                page = elem.getparent().getparent()
                ns = page.find(tag("ns"))
                if ns is not None and ns.text == "0":
                    etys += parse_element(elem)
                    words += 1
                    print(words, etys)
                page.clear()


def parse_element(elem: Element):
    i = 0
    word = elem.getparent().getparent().find(tag("title")).text
    print(word)
    wikitext = mwp.parse(elem.text)
    for language_section in wikitext.get_sections(levels=[2]):
        etymologies = language_section.get_sections(matches="Etymology", flat=True)
        for e in etymologies:
            clean_wikicode(e)
            i += sum([1 for n in e.ifilter_templates() if get_template_parser(str(n.name))])
    return i


def clean_wikicode(wc: Wikicode):
    """
    Performs operations on each etymology section that get rid of extraneous nodes
    and create new templates based on natural-lanugage parsing.
    """
    cleaner = lambda x: ((not isinstance(x, (Text, Wikilink, Template))) or
                         (isinstance(x, Text) and not bool(x.value.strip())))
    for node in wc.filter(recursive=False, matches=cleaner):
        wc.remove(node)

    merge_etyl_templates(wc)
    get_plus_combos(wc)
    get_comma_combos(wc)
    get_from_chains(wc)


def combine_template_chains(wc: Wikicode, new_template_name: str,
                            template_indices: List[int], text_indices: List[int]) -> None:
    index_combos = []

    index_combo = []
    combine = False
    for i in template_indices:
        if (i+1 in text_indices) or (i-2 in index_combo and combine):
            index_combo.append(i)

        combine = i+1 in text_indices
        if not combine:
            if len(index_combo) > 1:
                index_combos.append(index_combo)
            index_combo = []

    if len(index_combo) > 1:
        index_combos.append(index_combo)

    combo_nodes = [[wc.nodes[i] for i in chain] for chain in index_combos]

    for combo in combo_nodes:
        params = [Parameter(str(i), t) for i, t in enumerate(combo)]
        new_template = Template(new_template_name, params=params)
        wc.insert_before(combo[0], new_template, recursive=False)
        for node in combo:
            wc.remove(node, recursive=False)


def merge_etyl_templates(wc: Wikicode) -> Wikicode:
    """
    Given a chunk of wikicode, finds instances where the deprecated `etyl` template is immediately followed by
    either a word in free text, a linked word, or a generic `mention`/`link`/`langname-mention` template.
    It replaces this pattern with a new `derived-parsed` template -- meaning the same thing as the `derived` template
    but namespaced to differentiate. For cases where the `mention` language is different from the `etyl` language,
    we use the former. The template is removed if we can't parse it effectively.
    """
    etyl_indices = [i for i, node in enumerate(wc.nodes)
                    if isinstance(node, Template) and node.name == "etyl" and i < len(wc.nodes) - 1]

    nodes_to_remove = []
    for i in etyl_indices:
        make_new_template = False
        etyl: Template = wc.nodes[i]
        related_language = etyl.params[0]
        if len(etyl.params) == 1:
            language = "en"
        else:
            language = etyl.params[1]
        node = wc.nodes[i+1]
        if isinstance(node, Text):
            val = re.split(",| |", node.value.strip())[0]
            if val:
                make_new_template = True
        elif isinstance(node, Wikilink):
            val = node.text or node.title
            val = re.split(",| |", val.strip())[0]
            if val:
                make_new_template = True
        elif isinstance(node, Template):
            if node.name in ("m", "mention", "m+", "langname-mention", "l", "link"):
                related_language = node.params[0]
                if len(node.params) > 1:
                    val = node.params[1].value
                    make_new_template = True
                    nodes_to_remove.append(node)

        if make_new_template:
            params = [Parameter(str(i), str(param)) for i, param in enumerate([language, related_language, val])]
            new_template = Template("derived-parsed", params=params)
            wc.replace(etyl, new_template, recursive=False)
        else:
            nodes_to_remove.append(etyl)

    for node in nodes_to_remove:
        wc.remove(node, recursive=False)
    return wc


def get_comma_combos(wc: Wikicode) -> None:
    """
    Given a chunk of wikicode, finds templates separated by the symbol ",", which indicates morphemes
    related to both each other and the original word. It combines them into a single nested template, `related-parsed`.
    """
    template_indices = [i for i, node in enumerate(wc.nodes) if isinstance(node, Template)]
    text_indices = [i for i, node in enumerate(wc.nodes) if isinstance(node, Text) and str(node).strip() == ","]

    combine_template_chains(wc, new_template_name="related-parsed", template_indices=template_indices,
                            text_indices=text_indices)


def get_plus_combos(wc: Wikicode) -> None:
    """
    Given a chunk of wikicode, finds templates separated by the symbol "+", which indicates multiple
    morphemes that affix to make a single etymological relation. It combines these templates into a single nested
    `affix-parsed` template -- meaning the same thing as the `affix` template, but namespaced to differentiate.
    """
    template_indices = [i for i, node in enumerate(wc.nodes) if isinstance(node, Template)]
    text_indices = [i for i, node in enumerate(wc.nodes) if isinstance(node, Text) and str(node).strip() == "+"]

    combine_template_chains(wc, new_template_name="affix-parsed", template_indices=template_indices,
                            text_indices=text_indices)


def get_from_chains(wc: Wikicode) -> None:
    """
    Given a chunk of wikicode, finds templates separated by either "from" or ">", indicating an ordered chain
    of inheritance. It combines these templates into a single nested `from-parsed` template.
    """
    is_inheritance_str = lambda x: str(x).strip() == "<" or re.sub("[^a-z]+", "", str(x).lower()) == "from"

    template_indices = [i for i, node in enumerate(wc.nodes) if isinstance(node, Template)]
    text_indices = [i for i, node in enumerate(wc.nodes)
                    if isinstance(node, Text) and is_inheritance_str(node)]

    combine_template_chains(wc, new_template_name="from-parsed", template_indices=template_indices,
                            text_indices=text_indices)


def inherited(t: Template) -> Generator[List[str], None, None]:
    language = t.params[0]
    related_language = t.params[1]
    if len(t.params) > 2:
        related_word = t.params[2]
    else:
        related_word = None
    yield (language, related_language, related_word)


if __name__ == "__main__":
    download(WIKTIONARY_URL)
    stream_xml()
