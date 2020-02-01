"""Sentence Score"""
import kinda
from math import ceil
from typing import Optional
from ..constants import COMPOSITE_TOLERANCE, SENTENCE_SCORE_K
from ..repr_able import ReprAble


POSITION_SCORES = (.17, .23, .14, .08, .05, .04, .06, .04, .04, .15)


def calc_rank(index: int, total: int, num_ranks: int) -> int:
    """Get decile of `index` relative to `total`

    Raises:
        IndexError -- `index` out of range

    Returns:
        int -- decile of index (range: 1 to 10)
    """
    calc_idx = float(index)
    calc_of = float(total)

    try:
        decile = int(ceil((float(calc_idx) + 1) / calc_of * num_ranks))

        if 1 <= decile <= num_ranks:
            return decile

    except ZeroDivisionError:
        pass

    raise IndexError(f'invalid index {index} of {total}')


# Jagadeesh, J., Pingali, P., & Varma, V. (2005).
# Sentence Extraction Based Single Document Summarization.
# International Institute of Information Technology, Hyderabad, India, 5.
# pylint: disable=invalid-name
def score_position(index: int, of: int) -> float:
    """Score sentences[`index`] where len(sentences) = `of`

    Arguments:
        index {int} -- index of sentence in list
        of {int} -- length of sentence list

    Raises:
        IndexError -- invalid `index` for range(`of`)

    Returns:
        float -- score
    """
    score_index = calc_rank(index, of, len(POSITION_SCORES)) - 1

    return POSITION_SCORES[score_index]


# pylint: enable=invalid-name
def score_keyword_frequency(dbs_score: float, sbs_score: float) -> float:
    """Score keyword frequency

    Arguments:
        dbs_score {float} -- DBS score
        sbs_score {float} -- SBS score

    Returns:
        float -- keyword frequency score
    """
    return SENTENCE_SCORE_K * (sbs_score + dbs_score)


def score_total(
        title_score: float,
        keyword_score: float,
        length_score: float,
        position_score: float) -> float:
    """Calculate total score as composite of other scores

    Arguments:
        title_score {float} -- title score
        keyword_score {float} -- keyword frequency score
        length_score {float} -- sentence length score
        position_score {float} -- sentence position score

    Returns:
        float -- overall score
    """
    total = (
        title_score * 1.5 +
        keyword_score * 2.0 +
        length_score * 0.5 +
        position_score * 1.0) / 4.0

    return round(total / COMPOSITE_TOLERANCE) * COMPOSITE_TOLERANCE


class SentenceScore(ReprAble):
    def __init__(
            self,
            index: int,
            of: int,
            title_score: float,
            length_score: float,
            dbs_score: float,
            sbs_score: float) -> None:

        self._title = float(title_score)
        self._length = float(length_score)

        self._index = index
        self._of = of
        self._position = None  # type: Optional[float]

        self._dbs = float(dbs_score)
        self._sbs = float(sbs_score)
        self._keyword = None  # type: Optional[float]

        self._total = None    # type: Optional[float]

    @property
    def title(self) -> float:
        return self._title

    @property
    def length(self) -> float:
        return self._length

    @property
    def index(self) -> int:
        return self._index

    @property
    def of(self) -> int:
        return self._of

    @property
    def position(self):
        if self._position is None:
            self._position = score_position(self._index, self._of)

        return self._position

    @property
    def dbs(self) -> float:
        return self._dbs

    @property
    def sbs(self) -> float:
        return self._sbs

    @property
    def keyword(self) -> float:
        if self._keyword is None:
            self._keyword = score_keyword_frequency(self.dbs, self.sbs)

        return self._keyword

    @property
    def total(self) -> float:
        if self._total is None:
            self._total = score_total(
                self.title,
                self.keyword,
                self.length,
                self.position
            )

        return self._total

    def __lt__(self, other) -> bool:
        return self.total < other.total

    def __eq__(self, other) -> bool:
        equal = kinda.eq(
            self.total,
            other.total,
            abs_tol=COMPOSITE_TOLERANCE)

        return equal

    def __gt__(self, other) -> bool:
        return self.total > other.total

    def __str__(self) -> str:
        return str(self.total)

    def __repr__(self) -> str:
        return self._repr_(
            str(self.index),
            str(self.of),
            str(self.title),
            str(self.length),
            str(self.dbs),
            str(self.sbs)
        )
