"""Sentence string and score data"""
from typing import Tuple

from ..repr_able import ReprAble
from .sentence_score import SentenceScore


# pylint: disable=too-many-arguments,too-many-instance-attributes,invalid-name
class ScoredSentence(ReprAble):
    """Sentence data for summarization"""
    def _init_(
            self,
            text: str,
            index: int,
            total: int,
            tlds_scores: Tuple[float, float, float, float]) -> None:
        if (index >= total or index < 0):
            raise IndexError(': '.join([
                'sentence position out of bounds',
                f'range({total})[{index}]',
            ]))

        self._text = text
        self._index = index
        self._of = total
        self._score = SentenceScore(index, total, *tlds_scores)

    def __init__(
            self,
            text: str,
            index: int,
            total: int,
            tlds_scores: Tuple[float, float, float, float]) -> None:
        self._init_(
            str(text).strip(),
            round(index),
            round(total),
            tlds_scores
        )

    @property
    def text(self):
        return self._text

    @property
    def index(self):
        return self._index

    @property
    def of(self):
        return self._of

    @property
    def score(self):
        return self._score

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return self._repr_(
            self.text,
            self.index,
            self.of,
            (
                self.score.title,
                self.score.length,
                self.score.dbs,
                self.score.sbs,
            )
        )

    def __eq__(self, other) -> bool:
        return self.score.total == other.score.total

    def __lt__(self, other) -> bool:
        return self.score.total < other.score.total

    def __gt__(self, other) -> bool:
        return self.score.total > other.score.total
