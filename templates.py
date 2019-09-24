from enum import Enum
from typing import Callable

from mwparserfromhell.nodes.template import Template

from elements import Etymology


class RelType(Enum):
    Inherited = "inherited_from"
    Derived = "derived_from"
    Borrowed = "borrowed_from"
    LearnedBorrowing = "learned_borrowing_from"
    OrthographicBorrowing = "orthographic_borrowing_from"
    PieRoot = "has_pie_root"
    Affix = "has_affix"
    Prefix = "has_prefix"
    PrefixRoot = "has_prefix_with_root"
    Suffix = "has_suffix"
    SuffixRoot = "has_prefix_with_root"
    Confix = "has_confix"
    Compound = "compound_of"
    Blend = "blend_of"
    Clipping = "clipping_of"
    BackForm = "back-formation_from"
    Doublet = "doublet_with"
    Onomatopoeia = "is_onomatopoeic"
    Calque = "calque_of"
    SemanticLoan = "semantic_loan_of"
    NamedAfter = "named_after"
    PhonoSemanticMatching = "phono-semantic_matching_of"
    Mention = "etymologically_related_to"
    Cognate = "cognate_of"
    GroupAffix = "group_affix_root"
    GroupMention = "group_related_root"
    GroupDerived = "group_derived_root"


def get_template_parser(template_name: str) -> Callable[[str, str, Template], Etymology]:
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
    return parse_dict.get(template_name, lambda x, y, z: [])


def derived(term: str, lang: str, template: Template):
    """
    This template is a "catch-all" that is used when neither {{inherited}} nor {{borrowed}} is applicable.

    Params: (lang, source lang, source word)
    """
    p = [param for param in template.params if not param.showkey]
    if len(p) < 3:
        return []
    return Etymology(
        term=term,
        lang=lang,
        reltype=RelType.Derived.value,
        related_lang=str(p[1]),
        related_term=str(p[2])
    )


def borrowed(term: str, lang: str, template: Template):
    """
    This template is for loanwords that were borrowed during the time the borrowing language was spoken.

    Params: (lang, source lang, source word)
    """
    p = [param for param in template.params if not param.showkey]
    if len(p) < 3:
        return []
    return Etymology(
        term=term,
        lang=lang,
        reltype=RelType.Borrowed.value,
        related_lang=str(p[1]),
        related_term=str(p[2])
    )


def learned_borrowing(term: str, lang: str, template: Template):
    """
    This template is intended specifically for learned borrowings, those that were intentionally taken into a language
    from another not through normal means of language contact.

    Params: (lang, source lang, source word)
    """
    p = [param for param in template.params if not param.showkey]
    if len(p) < 3:
        return []
    return Etymology(
        term=term,
        lang=lang,
        reltype=RelType.LearnedBorrowing.value,
        related_lang=str(p[1]),
        related_term=str(p[2])
    )


def orthographic_borrowing(term: str, lang: str, template: Template):
    """
    This template is intended specifically for loans from language A into language B, which are loaned only in its
    script form and not pronunciation and often become new words which are phonetically quite dissimilar.

    Params: (lang, source lang, source word)
    """
    p = [param for param in template.params if not param.showkey]
    if len(p) < 3:
        return []
    return Etymology(
        term=term,
        lang=lang,
        reltype=RelType.OrthographicBorrowing.value,
        related_lang=str(p[1]),
        related_term=str(p[2])
    )


def inherited(term: str, lang: str, template: Template):
    """
    This template is intended for terms that have an unbroken chain of inheritance from the source term in question.

    Params: (lang, source lang, source word)
    """
    p = [param for param in template.params if not param.showkey]
    if len(p) < 3:
        return []
    return Etymology(
        term=term,
        lang=lang,
        reltype=RelType.Inherited.value,
        related_lang=str(p[1]),
        related_term=str(p[2])
    )


def pie_root(term: str, lang: str, template: Template):
    """
    This template adds entries to a subcategory of Category:Terms derived from Proto-Indo-European roots.

    Params: (lang, PIE root 1, PIE root n...)
    """
    p = [param for param in template.params if not param.showkey]
    etys = []
    for i, root in enumerate(p[1:]):
        etys.append(
            Etymology(
                term=term,
                lang=lang,
                reltype=RelType.PieRoot.value,
                related_lang="ine-pro",
                related_term=str(root),
                position=i
            ))
    return etys


def affix(term: str, lang: str, template: Template):
    """
    This template shows the parts (morphemes) that make up a word.

    Params: (lang, word part 1, word part n....)
    """
    p = [param for param in template.params if not param.showkey]
    etys = []
    for i, root in enumerate(p[1:]):
        etys.append(
            Etymology(
                term=term,
                lang=lang,
                reltype=RelType.Affix.value,
                related_lang=str(p[0]),
                related_term=str(root),
                position=i
            ))
    return etys


def prefix(term: str, lang: str, template: Template):
    """
    This template shows the parts (morphemes) that make up a word.

    Params: (lang, prefix, root)
    """
    p = [param for param in template.params if not param.showkey]
    pre = Etymology(
        term=term,
        lang=lang,
        reltype=RelType.Prefix.value,
        related_lang=str(p[0]),
        related_term=str(p[1])
    )
    if len(p) > 2 and str(p[2]):
        root = Etymology(
            term=term,
            lang=lang,
            reltype=RelType.PrefixRoot.value,
            related_lang=str(p[0]),
            related_term=str(p[2])
        )
        return [pre, root]
    else:
        return pre


def confix(term: str, lang: str, template: Template):
    """
    For use in the Etymology sections of words which consist of only a prefix and a suffix, or which were formed by
    simultaneous application of a prefix and a suffix to some other element(s).

    Params: (lang, prefix, confix root 1, confix root n..., suffix)
    """
    p = [param for param in template.params if not param.showkey]
    etys = []
    etys.append(
        Etymology(
            term=term,
            lang=lang,
            reltype=RelType.Confix.value,
            related_lang=str(p[0]),
            related_term=str(p[1]),
            position=0
        ))

    for i, root in enumerate(p[2:-1]):
        etys.append(
            Etymology(
                term=term,
                lang=lang,
                reltype=RelType.Confix.value,
                related_lang=str(p[0]),
                related_term=str(root),
                position=i+1
            ))

    etys.append(
        Etymology(
            term=term,
            lang=lang,
            reltype=RelType.Confix.value,
            related_lang=str(p[0]),
            related_term=str(p[-1]),
            position=len(p)-2
        ))
    return etys


def suffix(term: str, lang: str, template: Template):
    """
    This template shows the parts (morphemes) that make up a word.

    Params: (lang, root, suffix)
    """
    p = template.params
    suf = Etymology(
        term=term,
        lang=lang,
        reltype=RelType.Suffix.value,
        related_lang=str(p[0]),
        related_term=str(p[2])
    )
    root = Etymology(
        term=term,
        lang=lang,
        reltype=RelType.SuffixRoot.value,
        related_lang=str(p[0]),
        related_term=str(p[1])
    )
    return [root, suf]


def compound(term: str, lang: str, template: Template):
    """
    This template is used in the etymology section to display etymologies for compound words: words that are made up of
    multiple parts.

    Params: (source lang, word part 1, word part n...)
    """
    p = [param for param in template.params if not param.showkey]
    etys = []
    for i, root in enumerate(p[1:]):
        etys.append(
            Etymology(
                term=term,
                lang=lang,
                reltype=RelType.Compound.value,
                related_lang=str(p[0]),
                related_term=str(root),
                position=i
            ))
    return etys


def blend(term: str, lang: str, template: Template):
    """
    A word or name that combines two words, typically starting with the start of one word and ending with the end of
    another, such as smog (from smoke and fog) or Wiktionary (from wiki and dictionary). Many blends are portmanteaus.

    Params: (lang, word part 1, word part n...)
    """
    p = [param for param in template.params if not param.showkey]
    etys = []
    for i, root in enumerate(p[1:]):
        etys.append(
            Etymology(
                term=term,
                lang=lang,
                reltype=RelType.Blend.value,
                related_lang=str(p[0]),
                related_term=str(root),
                position=i
            ))
    return etys


def clipping(term: str, lang: str, template: Template):
    """
    A shortening of a word, without changing meaning or part of speech.

    Params: (lang, source word)
    """
    p = [param for param in template.params if not param.showkey]
    if len(p) < 2:
        return []
    return Etymology(
        term=term,
        lang=lang,
        reltype=RelType.Clipping.value,
        related_lang=str(p[0]),
        related_term=str(p[1])
    )


def back_form(term: str, lang: str, template: Template):
    """
    A term formed by removing an apparent or real prefix or suffix from an older term; for example, the noun pea arose
    because the final /z/ sound in pease sounded like a plural suffix. Similarly, the verb edit is a back-formation from
    the earlier noun editor. Not to be confused with clipping, which just shortens a word without changing meaning or
    part of speech.

    Params: (lang, source word)
    """
    p = [param for param in template.params if not param.showkey]
    if len(p) < 2:
        return []
    return Etymology(
        term=term,
        lang=lang,
        reltype=RelType.BackForm.value,
        related_lang=str(p[0]),
        related_term=str(p[1])
    )


def doublet(term: str, lang: str, template: Template):
    """
    In etymology, two or more words in the same language are called doublets or etymological twins or twinlings
    (or possibly triplets, and so forth) when they have different phonological forms but the same etymological root.

    Params: (lang, word part 1, word part n...)
    """
    p = [param for param in template.params if not param.showkey]
    etys = []
    for i, doub in enumerate(p[1:]):
        etys.append(
            Etymology(
                term=term,
                lang=lang,
                reltype=RelType.Doublet.value,
                related_lang=str(p[0]),
                related_term=str(doub),
                position=i
            ))
    return etys


def onomatopoeic(term: str, lang: str, template: Template):
    """
    This templates indicates that a word is an onomatopoeia.

    Params: (lang)
    """
    p = [param for param in template.params if not param.showkey]
    return Etymology(
        term=term,
        lang=lang,
        reltype=RelType.Onomatopoeia.value,
        related_lang=str(p[0]),
        related_term=term
    )


def calque(term: str, lang: str, template: Template):
    """
    In linguistics, a calque or loan translation is a word or phrase borrowed from another language by literal,
    word-for-word or root-for-root translation.

    Params: (lang, source lang, source word)
    """
    p = [param for param in template.params if not param.showkey]
    if len(p) < 3:
        return []
    return Etymology(
        term=term,
        lang=lang,
        reltype=RelType.Calque.value,
        related_lang=str(p[1]),
        related_term=str(p[2])
    )


def semantic_loan(term: str, lang: str, template: Template):
    """
    Semantic borrowing is a special case of calque or loan-translation, in which the word in the borrowing
    language already existed and simply had a new meaning added to it.

    Params: (lang, source lang, source word)
    """
    p = [param for param in template.params if not param.showkey]
    if len(p) < 3:
        return []
    return Etymology(
        term=term,
        lang=lang,
        reltype=RelType.SemanticLoan.value,
        related_lang=str(p[1]),
        related_term=str(p[2])
    )


def named_after(term: str, lang: str, template: Template):
    """
    Use this template in an etymology section of eponyms.

    Params: (lang, person's name)
    """
    p = [param for param in template.params if not param.showkey]
    if len(p) < 2:
        return []
    return Etymology(
        term=term,
        lang=lang,
        reltype=RelType.NamedAfter.value,
        related_lang=str(p[0]),
        related_term=str(p[1])
    )


def phono_semantic_matching(term: str, lang: str, template: Template):
    """
    Phono-semantic matching (PSM) is the incorporation of a word into one language from another, often creating
    a neologism, where the word's non-native quality is hidden by replacing it with phonetically and semantically
    similar words or roots from the adopting language. Thus, the approximate sound and meaning of the original
    expression in the source language are preserved, though the new expression (the PSM) in the target language may
    sound native.

    Params: (lang, source lang, source word)
    """
    p = [param for param in template.params if not param.showkey]
    if len(p) < 3:
        return []
    return Etymology(
        term=term,
        lang=lang,
        reltype=RelType.PhonoSemanticMatching.value,
        related_lang=str(p[1]),
        related_term=str(p[2])
    )


def mention(term: str, lang: str, template: Template):
    """
    Use this template when a particular term is mentioned within running English text.

    Params: (source lang, source word)
    """
    p = [param for param in template.params if not param.showkey]
    if len(p) < 2:
        return []
    return Etymology(
        term=term,
        lang=lang,
        reltype=RelType.Mention.value,
        related_lang=str(p[0]),
        related_term=str(p[1])
    )


def cognate(term: str, lang: str, template: Template):
    """
    This template is used to indicate cognacy with terms in other languages that are not ancestors of the given term
    (hence none of {{inherited}}, {{borrowed}}, and {{derived}} are applicable).
    There is no consensus whether its use for etymologically related but borrowed terms is appropriate.

    Params: (source lang, source word)
    """
    p = [param for param in template.params if not param.showkey]
    if len(p) < 2:
        return []
    return Etymology(
        term=term,
        lang=lang,
        reltype=RelType.Cognate.value,
        related_lang=str(p[0]),
        related_term=str(p[1])
    )


def non_cognate(term: str, lang: str, template: Template):
    """
    This template is used to format terms in other languages that are mentioned in etymology sections
    but are not cognate with the page's term.

    Params: (source lang, source word)
    """
    p = [param for param in template.params if not param.showkey]
    if len(p) < 2:
        return []
    return Etymology(
        term=term,
        lang=lang,
        reltype=RelType.Mention.value,
        related_lang=str(p[0]),
        related_term=str(p[1])
    )


def derived_parsed(term: str, lang: str, template: Template):
    """
    Same as derived, but a custom solution that automatically parses etyl templates in which the word is located
    outside of the template.

    Params: (lang, source lang, source word)
    """
    p = [param for param in template.params if not param.showkey]
    return Etymology(
        term=term,
        lang=lang,
        reltype=RelType.Derived.value,
        related_lang=str(p[1]),
        related_term=str(p[2])
    )


def unnest_template(term: str, lang: str, template: Template, reltype: RelType):
    """
    Builds etymologies out of nested templates, assigning the immediate parent to a given child
    in cases of deeply nested templates.
    """
    parent_index = 0
    parent_ety = Etymology(
        term=term,
        lang=lang,
        reltype=reltype.value,
        related_lang=None,
        related_term=None,
        root_tag=Etymology.generate_root_tag()
    )
    etys = [parent_ety]
    for p in template.params:
        for child_template in p.value.filter_templates(recursive=False):
            parser = get_template_parser(str(child_template.name))
            if parser:
                child_etys = parser(term, lang, child_template)
                child_etys = [child_etys] if isinstance(child_etys, Etymology) else child_etys
                for child_ety in child_etys:
                    if child_ety.parent_tag:
                        # This means the template was at least doubly nested and a parent has already been assigned
                        # further up the stack
                        etys.append(child_ety)
                    else:
                        parented_ety = Etymology.with_parent(child=child_ety, parent=parent_ety, position=parent_index)
                        etys.append(parented_ety)
                parent_index += 1
    return etys


def affix_parsed(term: str, lang: str, template: Template):
    """
    Same as affix, but a custom solution that parses plain text to find strings of "+" - separated terms.

    Child templates are extracted and linked hierarchically.
    Params: (Template 1, template n...)
    """
    return unnest_template(term=term, lang=lang, template=template, reltype=RelType.GroupAffix)


def from_parsed(term: str, lang: str, template: Template):
    """
    Custom solution that finds chains of derivation.

    Child templates are extracted and linked hierarchically.
    Params: (Template 1, template n...)
    """
    return unnest_template(term=term, lang=lang, template=template, reltype=RelType.GroupDerived)


def related_parsed(term: str, lang: str, template: Template):
    """
    Custom solution to find morphemes related to both each other and the original word.

    Child templates are extracted and linked hierarchically.
    Params: (Template 1, template n...)
    """
    return unnest_template(term=term, lang=lang, template=template, reltype=RelType.GroupMention)

