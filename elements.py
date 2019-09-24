import csv
import uuid, base64
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional, Tuple, Dict

LANG_CODE_PATH = Path.cwd().joinpath("wiktionary_codes.csv")


@dataclass(frozen=True)
class Etymology:
    lang: str
    term: str
    reltype: str
    related_lang: Optional[str]
    related_term: Optional[str]
    position: int = 0
    group_tag: str = None
    parent_tag: str = None
    parent_position: int = None

    @classmethod
    def with_parent(cls, child: "Etymology", parent: "Etymology", position: int = 0):
        return cls(lang=child.lang, term=child.term, reltype=child.reltype, related_lang=child.related_lang,
                   related_term=child.related_term, position=child.position, group_tag=child.group_tag,
                   parent_tag=parent.group_tag, parent_position=position)

    @staticmethod
    def make_uuid(*terms):
        uuid_id = uuid.uuid5(uuid.NAMESPACE_OID, "^".join((str(t) for t in terms)))
        return base64.urlsafe_b64encode(uuid_id.bytes).decode("ascii").rstrip("=")

    @property
    def term_id(self) -> str:
        return self.make_uuid(self.lang, self.term)

    @property
    def related_term_id(self) -> Optional[str]:
        if not (self.related_lang_full and self.related_term):
            return
        return self.make_uuid(self.related_lang_full, self.related_term)

    @staticmethod
    def generate_root_tag() -> str:
        uuid_id = uuid.uuid4()
        return base64.urlsafe_b64encode(uuid_id.bytes).decode("ascii").rstrip("=")

    @property
    def related_lang_full(self):
        return lang_dict().get(self.related_lang, self.related_lang)

    def is_valid(self) -> bool:
        # May include more conditions in the future
        return self.related_term not in ("", "-")

    @staticmethod
    def header() -> Tuple[str, ...]:
        h = ("term_id", "lang", "term", "reltype", "related_term_id", "related_lang",
             "related_term", "position", "group_tag", "parent_tag", "parent_position")
        return h

    def to_row(self) -> Tuple[str, str, str, str, Optional[str], Optional[str], Optional[str], int, Optional[str],
                              Optional[str], Optional[int]]:
        row = (self.term_id, self.lang, self.term, self.reltype, self.related_term_id, self.related_lang_full,
               self.related_term, self.position, self.group_tag, self.parent_tag, self.parent_position)
        return row


@lru_cache(maxsize=1)
def lang_dict() -> Dict[str, str]:
    with open(LANG_CODE_PATH, 'r') as f_in:
        reader = csv.reader(f_in)
        next(reader)
        return {row[0]: row[1] for row in reader}
