"""Keyword string and score data"""
import typing

import kinda

from ..constants import KEYWORD_SCORE_K
from ..repr_able import ReprAble


def score_keyword(count: int, of: int) -> float:
    """Score keyword by frequency in content body

    Arguments:
        count {int} -- number of appearances in content
        of {int} -- total number of keywords in content

    Returns:
        float -- keyword score
    """
    if (count < 0) or (of < 1) or (of < count):
        raise ValueError('invalid word count ({!r} of {!r})'.format(count, of))

    return KEYWORD_SCORE_K * count / of


def compare_score(a: float, b: float) -> int:
    """Compare score property of `a` to `b` (unambiguous)

    Arguments:
        a {float} -- keyword score
        b {float} -- keyword score

    Returns:
        int -- `a lt b`: -1, `a eq b`: 0, `a gt b`: 1
    """
    if kinda.eq(a, b):
        return 0

    if (a < b):
        return -1

    return 1


def compare_word(a: str, b: str) -> int:
    """Compare word property of `a` to `b` (unambiguous)

    Arguments:
        a {ScoredKeyword} -- keyword
        b {ScoredKeyword} -- keyword

    Returns:
        int -- `a lt b`: -1, `a eq b`: 0, `a gt b`: 1
    """
    if (a == b):
        return 0

    if (a < b):
        return -1

    return 1


class ScoredKeyword(ReprAble):
    __slots__ = ['word', 'count', 'of', 'score']

    def __init__(self, word: str, count: int, of: int) -> None:
        self.word = str(word).lower()
        self.count = int(count)
        self.of = int(of)
        self.score = score_keyword(self.count, self.of)

    def __str__(self) -> str:
        return self.word

    def __repr__(self) -> str:
        return self._repr_(self.word, self.count, self.of)

    def __lt__(self, other) -> bool:
        cmp = compare_keywords(self, other)

        return (cmp < (0, 0, 0))

    def __eq__(self, other) -> bool:
        cmp = compare_keywords(self, other)

        return (cmp == (0, 0, 0))

    def __gt__(self, other) -> bool:
        cmp = compare_keywords(self, other)

        return (cmp > (0, 0, 0))


def compare_keywords(
        a: ScoredKeyword,
        b: ScoredKeyword
        ) -> typing.Tuple[int, int, int]:
    """Compare properties of `a` to `b` (unambiguous)

    Arguments:
        a {ScoredKeyword} -- keyword
        b {ScoredKeyword} -- keyword

    Returns:
        tuple[int, int, int] -- abstract value of ScoredKeyword `a` - `b`
    """
    return (
        compare_score(a.score, b.score),
        len(a.word) - len(b.word),
        compare_word(a.word, b.word), )
