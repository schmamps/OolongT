from math import ceil

from oolongt import roughly
from oolongt.constants import KEYWORD_SCORE_K
from oolongt.typing.repr_able import ReprAble


def score_keyword(count, of):
    # type: (int, int) -> float
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


def compare_score(a, b):
    # type: (ScoredKeyword, ScoredKeyword) -> int
    """Compare score property of ScoredKeyword `a` to `b`

    Arguments:
        a {ScoredKeyword} -- keyword
        b {ScoredKeyword} -- keyword

    Returns:
        int -- a.score - b.score (0 if equivalent floats)
    """
    if roughly.eq(a.score, b.score):
        return 0

    if (a.score < b.score):
        return -1

    return 1


def compare_length(a, b):
    # type: (ScoredKeyword, ScoredKeyword) -> int
    """Compare length of ScoredKeyword.word `a` to `b`

    Arguments:
        a {ScoredKeyword} -- keyword
        b {ScoredKeyword} -- keyword

    Returns:
        int -- difference in length (a-b)
    """
    return len(a.word) - len(b.word)


def compare_word(a, b):
    # type: (ScoredKeyword, ScoredKeyword) -> int
    """Compare word property of ScoredKeyword `a` to `b`

    Arguments:
        a {ScoredKeyword} -- keyword
        b {ScoredKeyword} -- keyword

    Returns:
        int -- abstract value of `a.word` - `b.word`
    """
    if (a.word == b.word):
        return 0

    if (a.word < b.word):
        return -1

    return 1


def compare_keywords(a, b):
    # type: (ScoredKeyword, ScoredKeyword) -> int
    """Compare ScoredKeyword `a` to ScoredKeyword `b`

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


class ScoredKeyword(ReprAble):
    __slots__ = ['word', 'count', 'of', 'score']

    def __init__(self, word, count, of):
        # type: (str, int, int) -> None
        self.word = str(word).lower()
        self.count = int(count)
        self.of = int(of)
        self.score = score_keyword(self.count, self.of)

    def __str__(self):
        return self.word

    def __repr__(self):
        return self._repr_(self.word, self.count, self.of)

    def __eq__(self, other):
        cmp = compare_keywords(self, other)

        return (cmp == (0, 0, 0))

    def __lt__(self, other):
        cmp = compare_keywords(self, other)

        return (cmp < (0, 0, 0))

    def __gt__(self, other):
        cmp = compare_keywords(self, other)

        return (cmp > (0, 0, 0))

    def __ne__(self, other):
        return not (self == other)

    def __le__(self, other):
        return (self < other) or (self == other)

    def __ge__(self, other):
        return (self > other) or (self == other)
