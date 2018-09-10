"""Sentence string and score data"""
from math import ceil

import kinda

from ..constants import COMPOSITE_TOLERANCE, SENTENCE_SCORE_K
from ..repr_able import ReprAble


# pylint: disable=invalid-name
def calc_decile(index: int, of: int) -> int:
    """Get decile of `index` relative to `of`

    Raises:
        IndexError -- `index` out of range

    Returns:
        int -- decile of index (range: 1 to 10)
    """
    calc_idx = float(index)
    calc_of = float(of)

    try:
        decile = int(ceil((float(calc_idx) + 1) / calc_of * 10))

        if 1 <= decile <= 10:
            return decile

    except ZeroDivisionError:
        pass

    raise IndexError(
        'Invalid index/of ({0}/{1})'.format(index, of))


# Jagadeesh, J., Pingali, P., & Varma, V. (2005).
# Sentence Extraction Based Single Document Summarization.
# International Institute of Information Technology, Hyderabad, India, 5.
def score_position(index: int, of: int) -> float:
    """Score sentences[`index`] where len(sentences) = `sentence_count`

    Arguments:
        index {int} -- index of sentence in list
        sentence_count {int} -- length of sentence list

    Raises:
        IndexError -- invalid `index` for range(`of`)

    Returns:
        float -- score
    """
    score_index = calc_decile(index, of) - 1

    return (.17, .23, .14, .08, .05, .04, .06, .04, .04, .15)[score_index]


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
    return (
        title_score * 1.5 +
        keyword_score * 2.0 +
        length_score * 0.5 +
        position_score * 1.0) / 4.0


# pylint: disable=too-many-arguments,too-many-instance-attributes
class ScoredSentence(ReprAble):
    """Sentence data for summarization"""
    __slots__ = [
        'text', 'index', 'of',
        'title_score', 'length_score',
        'dbs_score', 'sbs_score',
        'position_score', 'keyword_score', 'total_score', ]

    def _init_(
            self,
            text: str,
            index: int,
            of: int,
            title_score: float,
            length_score: float,
            dbs_score: float,
            sbs_score: float,
            keyword_score: float,
            position_score: float,
            total_score: float) -> None:
        self.text = str(text)
        self.index = round(index)
        self.of = round(of)
        self.title_score = float(title_score)
        self.length_score = float(length_score)
        self.dbs_score = float(dbs_score)
        self.sbs_score = float(sbs_score)
        self.position_score = float(position_score)
        self.keyword_score = float(keyword_score)
        self.total_score = float(total_score)

    def __init__(
            self,
            text: str,
            index: int,
            of: int,
            title_score: float,
            length_score: float,
            dbs_score: float,
            sbs_score: float) -> None:
        index = round(index)
        of = round(of)

        position_score = score_position(
            index, of)
        keyword_score = score_keyword_frequency(
            dbs_score, sbs_score)
        total_score = score_total(
            title_score, keyword_score, length_score, position_score)

        self._init_(
            text, index, of,
            title_score, length_score,
            dbs_score, sbs_score, keyword_score,
            position_score, total_score)

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return self._repr_(
            self.text,
            self.index,
            self.of,
            self.title_score,
            self.length_score,
            self.dbs_score,
            self.sbs_score)

    def __eq__(self, other) -> bool:
        return kinda.eq(
            self.total_score, other.total_score, rel_tol=COMPOSITE_TOLERANCE)

    def __lt__(self, other) -> bool:
        return kinda.lt(
            self.total_score, other.total_score, rel_tol=COMPOSITE_TOLERANCE)

    def __gt__(self, other) -> bool:
        return kinda.gt(
            self.total_score, other.total_score, rel_tol=COMPOSITE_TOLERANCE)
