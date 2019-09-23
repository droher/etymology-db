from typing import Callable

from mwparserfromhell.nodes.template import Template

from elements import Etymology


def get_template_parser(template_name: str) -> Callable[[Template], ...]:
    parse_dict = {
        "inherited": inherited,
        "inh": inherited,
        "derived": derived,
        "der": derived,
        "borrowed": borrowed,
        "bor": borrowed,
        "learned borrowring": learned_borrowing,
        "orthographic borrowing": orthographic_borrowing,
        "obor": orthographic_borrowing,
        "PIE root": pie_root,
        "affix": affix,
        "af": affix,
        "prefix": prefix,
        "confix": confix,
        "suffix": suffix,
        "compound": compound,
        "blend": blend,
        "clipping": clipping,
        "back_form": back_form,
        "doublet": doublet,
        "onomatopoeic": onomatopoeic,
        "onom": onomatopoeic,
        "calque": calque,
        "semantic loan": semantic_loan,
        "named-after": named_after,
        "phono-semantifc matching": phono_semantic_matching,
        "psm": phono_semantic_matching,
        "mention": mention,
        "m": mention,
        "cognate": cognate,
        "cog": cognate,
        "noncognate": non_cognate,
        "noncog": non_cognate,
        "langname-mention": mention,
        "m+": mention,
        "link": mention,
        "l": mention,
        "derived-parsed": derived_parsed,
        "affix-parsed": affix_parsed,
        "from-parsed": from_parsed,
        "related-parsed": related_parsed
    }
    return parse_dict.get(template_name)


def derived(template: Template):
    """
    This template is a "catch-all" that is used when neither {{inherited}} nor {{borrowed}} is applicable.

    Params: (lang, source lang, source word)
    """
    pass


def borrowed(template: Template):
    """
    This template is for loanwords that were borrowed during the time the borrowing language was spoken.

    Params: (lang, source lang, source word)
    """
    pass


def learned_borrowing(template: Template):
    """
    This template is intended specifically for learned borrowings, those that were intentionally taken into a language
    from another not through normal means of language contact.

    Params: (lang, source lang, source word)
    """
    pass


def orthographic_borrowing(template: Template):
    """
    This template is intended specifically for loans from language A into language B, which are loaned only in its
    script form and not pronunciation and often become new words which are phonetically quite dissimilar.

    Params: (lang, source lang, source word)
    """
    pass


def inherited(template: Template):
    """
    This template is intended for terms that have an unbroken chain of inheritance from the source term in question.

    Params: (lang, source lang, source word)
    """
    pass


def pie_root(template: Template):
    """
    This template adds entries to a subcategory of Category:Terms derived from Proto-Indo-European roots.

    Params: (lang, PIE root 1, PIE root n...)
    """
    pass


def affix(template: Template):
    """
    This template shows the parts (morphemes) that make up a word.

    Params: (lang, word part 1, word part n....)
    """
    pass


def prefix(template: Template):
    """
    This template shows the parts (morphemes) that make up a word.

    Params: (lang, prefix, root)
    """
    pass


def confix(template: Template):
    """
    For use in the Etymology sections of words which consist of only a prefix and a suffix, or which were formed by
    simultaneous application of a prefix and a suffix to some other element(s).

    Params: (lang, prefix, suffix)
    """
    pass


def suffix(template: Template):
    """
    This template shows the parts (morphemes) that make up a word.

    Params: (lang, root, suffix)
    """
    pass


def compound(template: Template):
    """
    This template is used in the etymology section to display etymologies for compound words: words that are made up of
    multiple parts.

    Params: (source lang, word part 1, word part n...)
    """
    pass


def blend(template: Template):
    """
    A word or name that combines two words, typically starting with the start of one word and ending with the end of
    another, such as smog (from smoke and fog) or Wiktionary (from wiki and dictionary). Many blends are portmanteaus.

    Params: (lang, word part 1, word part n...)
    """
    pass


def clipping(template: Template):
    """
    A shortening of a word, without changing meaning or part of speech.

    Params: (lang, source word)
    """
    pass


def back_form(template: Template):
    """
    A term formed by removing an apparent or real prefix or suffix from an older term; for example, the noun pea arose
    because the final /z/ sound in pease sounded like a plural suffix. Similarly, the verb edit is a back-formation from
    the earlier noun editor. Not to be confused with clipping, which just shortens a word without changing meaning or
    part of speech.

    Params: (lang, source word)
    """
    pass


def doublet(template: Template):
    """
    In etymology, two or more words in the same language are called doublets or etymological twins or twinlings
    (or possibly triplets, and so forth) when they have different phonological forms but the same etymological root.

    Params: (lang, word part 1, word part n...)
    """
    pass


def onomatopoeic(template: Template):
    """
    This templates indicates that a word is an onomatopoeia.

    Params: (lang)
    """
    pass


def calque(template: Template):
    """
    In linguistics, a calque or loan translation is a word or phrase borrowed from another language by literal,
    word-for-word or root-for-root translation.

    Params: (lang, source lang, source word)
    """
    pass


def semantic_loan(template: Template):
    """
    Semantic borrowing is a special case of calque or loan-translation, in which the word in the borrowing
    language already existed and simply had a new meaning added to it.

    Params: (lang, source lang, source word)
    """
    pass


def named_after(template: Template):
    """
    Use this template in an etymology section of eponyms.

    Params: (lang, person's name)
    """
    pass


def phono_semantic_matching(template: Template):
    """
    Phono-semantic matching (PSM) is the incorporation of a word into one language from another, often creating
    a neologism, where the word's non-native quality is hidden by replacing it with phonetically and semantically
    similar words or roots from the adopting language. Thus, the approximate sound and meaning of the original
    expression in the source language are preserved, though the new expression (the PSM) in the target language may
    sound native.

    Params: (lang, source lang, source word)
    """
    pass


def mention(template: Template):
    """
    Use this template when a particular term is mentioned within running English text.

    Params: (source lang, source word)
    """
    pass


def cognate(template: Template):
    """
    This template is used to indicate cognacy with terms in other languages that are not ancestors of the given term
    (hence none of {{inherited}}, {{borrowed}}, and {{derived}} are applicable).
    There is no consensus whether its use for etymologically related but borrowed terms is appropriate.

    Params: (source lang, source word)
    """
    pass


def non_cognate(template: Template):
    """
    This template is used to format terms in other languages that are mentioned in etymology sections
    but are not cognate with the page's term.

    Params: (source lang, source word)
    """
    pass


def derived_parsed(template: Template):
    """
    Same as derived, but a custom solution that automatically parses etyl templates in which the word is located
    outside of the template.

    Params: (lang, source lang, source word)
    """
    pass


def affix_parsed(template: Template):
    """
    Same as affix, but a custom solution that parses plain text to find strings of "+" - separated terms.

    Child templates are extracted and linked hierarchically.
    Params: (Template 1, template n...)
    """
    pass


def from_parsed(template: Template):
    """
    Custom solution that finds chains of derivation.

    Child templates are extracted and linked hierarchically.
    Params: (Template 1, template n...)
    """
    pass


def related_parsed(template: Template):
    """
    Custom solution to find morphemes related to both each other and the original word.

    Child templates are extracted and linked hierarchically.
    Params: (Template 1, template n...)
    """
    pass
