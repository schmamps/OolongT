"""Keyword string and score data"""
import typing

import kinda

from ..constants import KEYWORD_SCORE_K
from ..repr_able import ReprAble


def score_keyword(  # pylint: disable=invalid-name
        count: int,
        of: int) -> float:
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


def compare_score(score_a: float, score_b: float) -> int:
    """Compare score property of `kw_a` to `kw_b` (unambiguous)

    Arguments:
        score_a {float} -- keyword score
        score_b {float} -- keyword score

    Returns:
        int --
            `score_a lt score_b`: -1,
            `score_a eq score_b`: 0,
            `score_a gt score_b`: 1
    """
    if kinda.eq(score_a, score_b):
        return 0

    if score_a < score_b:
        return -1

    return 1


def compare_word(word_a: str, word_b: str) -> int:
    """Compare word property of `word_a` to `word_b` (unambiguous)

    Arguments:
        word_a {ScoredKeyword} -- keyword
        word_b {ScoredKeyword} -- keyword

    Returns:
        int --
            `word_a lt word_b`: -1,
            `word_a eq word_b`: 0,
            `word_a gt word_b`: 1
    """
    if word_a == word_b:
        return 0

    if word_a < word_b:
        return -1

    return 1


class ScoredKeyword(ReprAble):
    """Keyword data"""
    __slots__ = ['word', 'count', 'of', 'score']

    def __init__(self, word: str, count: int, total: int) -> None:
        self.word = str(word).lower()
        self.count = int(count)
        self.of = int(total)  # pylint: disable=invalid-name
        self.score = score_keyword(self.count, self.of)

    def __str__(self) -> str:
        return self.word

    def __repr__(self) -> str:
        return self._repr_(self.word, self.count, self.of)

    def __lt__(self, other) -> bool:
        cmp = compare_keywords(self, other)

        return cmp < (0, 0, 0)

    def __eq__(self, other) -> bool:
        cmp = compare_keywords(self, other)

        return cmp == (0, 0, 0)

    def __gt__(self, other) -> bool:
        cmp = compare_keywords(self, other)

        return cmp > (0, 0, 0)


def compare_keywords(
        kw_a: ScoredKeyword,
        kw_b: ScoredKeyword) -> typing.Tuple[int, int, int]:
    """Compare properties of `kw_a` to `kw_b` (unambiguous)

    Arguments:
        kw_a {ScoredKeyword} -- keyword
        kw_b {ScoredKeyword} -- keyword

    Returns:
        tuple[int, int, int] -- abstract value of ScoredKeyword `kw_a` - `kw_b`
    """
    return (
        compare_score(kw_a.score, kw_b.score),
        len(kw_a.word) - len(kw_b.word),
        compare_word(kw_a.word, kw_b.word), )
