from typing import Callable


def get_template_parser(template_name: str) -> Callable:
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
        "prefix": prefix,
        "confix": confix,
        "suffix": suffix,
        "compound": compound,
        "blend": blend,
        "clipping": clipping,
        "short_for": short_for,
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
        "langname-mention": langname_mention,
        "m+": langname_mention,
        "link": link,
        "l": link,
        "derived-parsed": derived_parsed,
        "affix-parsed": affix_parsed,
        "from-parsed": from_parsed,
        "related-parsed": related_parsed
    }
    return parse_dict.get(template_name)


def derived():
    pass


def borrowed():
    pass


def learned_borrowing():
    pass


def orthographic_borrowing():
    pass


def inherited():
    pass


def pie_root():
    pass


def affix():
    pass


def prefix():
    pass


def confix():
    pass


def suffix():
    pass


def compound():
    pass


def blend():
    pass


def clipping():
    pass


def short_for():
    pass


def back_form():
    pass


def doublet():
    pass


def onomatopoeic():
    pass


def calque():
    pass


def semantic_loan():
    pass


def named_after():
    pass


def phono_semantic_matching():
    pass


def mention():
    pass


def cognate():
    pass


def non_cognate():
    pass


def langname_mention():
    pass


def etyl():
    pass


def link():
    pass


def derived_parsed():
    pass


def affix_parsed():
    pass


def from_parsed():
    pass


def related_parsed():
    pass
