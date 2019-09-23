import uuid, base64
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Etymology:
    lang: str
    word: str
    reltype: str
    related_lang: Optional[str]
    related_term: Optional[str]
    position: int = 0
    parent_id: str = None
    parent_reltype: str = None
    parent_position: int = None

    @classmethod
    def with_parent(cls, child: "Etymology", parent: "Etymology", position: int = 0):
        return cls(lang=child.lang, word=child.word, reltype=child.reltype, related_lang=child.related_lang,
                   related_term=child.related_term, position=child.position,
                   parent_id=parent.id, parent_reltype=parent.reltype, parent_position=position)

    @property
    def id(self) -> str:
        terms = self.lang, self.word, self.reltype, self.related_lang, self.related_term, self.position
        uuid_id = uuid.uuid5(uuid.NAMESPACE_OID, "^".join((str(t) for t in terms)))
        return base64.urlsafe_b64encode(uuid_id.bytes).decode("ascii").rstrip("=")
