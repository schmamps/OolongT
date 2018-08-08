"""Keyword string and score data"""
import typing
from math import ceil

from oolongt import roughly
from oolongt.constants import KEYWORD_SCORE_K
from oolongt.typedefs import ReprAble


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

    def __eq__(self, other) -> bool:
        cmp = compare_keywords(self, other)

        return (cmp == (0, 0, 0))

    def __lt__(self, other) -> bool:
        cmp = compare_keywords(self, other)

        return (cmp < (0, 0, 0))

    def __gt__(self, other) -> bool:
        cmp = compare_keywords(self, other)

        return (cmp > (0, 0, 0))

    def __ne__(self, other) -> bool:
        return not (self == other)

    def __le__(self, other) -> bool:
        return (self < other) or (self == other)

    def __ge__(self, other) -> bool:
        return (self > other) or (self == other)


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


def compare_score(a: ScoredKeyword, b: ScoredKeyword) -> int:
    """Compare score property of `a` to `b` (unambiguous)

    Arguments:
        a {ScoredKeyword} -- keyword
        b {ScoredKeyword} -- keyword

    Returns:
        int -- `a lt b`: -1, `a eq b`: 0, `a gt b`: 1
    """
    if roughly.eq(a.score, b.score):
        return 0

    if (a.score < b.score):
        return -1

    return 1


def compare_length(a: ScoredKeyword, b: ScoredKeyword) -> int:
    """Compare word length of `a` to `b`

    Arguments:
        a {ScoredKeyword} -- keyword
        b {ScoredKeyword} -- keyword

    Returns:
        int -- difference `a - b`
    """
    return len(a.word) - len(b.word)


def compare_word(a: ScoredKeyword, b: ScoredKeyword) -> int:
    """Compare word property of `a` to `b` (unambiguous)

    Arguments:
        a {ScoredKeyword} -- keyword
        b {ScoredKeyword} -- keyword

    Returns:
        int -- `a lt b`: -1, `a eq b`: 0, `a gt b`: 1
    """
    if (a.word == b.word):
        return 0

    if (a.word < b.word):
        return -1

    return 1


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
        compare_score(a, b),
        compare_length(a, b),
        compare_word(a, b), )
