from typing import List, Dict
from dataclasses import dataclass


@dataclass
class Etymology:
    id: int
    word: str
    language: str
    relation_type: str
    related_word: str = None
    related_language: str = None
    related_id: int = None

