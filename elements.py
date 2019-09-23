from dataclasses import dataclass


@dataclass(frozen=True)
class Etymology:
    id: int
    lang: str
    word: str
    reltype: str
    related_lang: str
    related_term: str
    position: int = None
    parent_id: int = None
    parent_reltype: str = None
    parent_position: str = None

