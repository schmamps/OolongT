from math import ceil, isclose

from oolongt import roughly
from oolongt.typing.repr_able import ReprAble


# Jagadeesh, J., Pingali, P., & Varma, V. (2005).
# Sentence Extraction Based Single Document Summarization.
# International Institute of Information Technology, Hyderabad, India, 5.
def score_position(index, of):
    # type: (int, int) -> float
    """Score sentences[`index`] where len(sentences) = `sentence_count`

    Arguments:
        index {int} -- index of sentence in list
        sentence_count {int} -- length of sentence list

    Returns:
        float -- score
    """
    POS_SCORES = [.17, .23, .14, .08, .05, .04, .06, .04, .04, .15]

    try:
        score_index = ceil((index + 1) / of * 10) - 1

        return POS_SCORES[score_index]

    except (IndexError, ZeroDivisionError):
        raise ValueError(' '.join([
            'Invalid index/sentence count: ',
            str(index),
            '/',
            str(of)]))


def score_keyword_frequency(dbs_score, sbs_score):
    K = 5.0

    return K * (sbs_score + dbs_score)


def score_total(title_score, keyword_score, length_score, position_score):
    return (
        title_score * 1.5 +
        keyword_score * 2.0 +
        length_score * 0.5 +
        position_score * 1.0) / 4.0


class ScoredSentence(ReprAble):
    __slots__ = [
        'text', 'index', 'of',
        'title_score', 'length_score',
        'dbs_score', 'sbs_score',
        'position_score', 'keyword_score', 'total_score', ]

    def _init_(
            self, text, index, of,
            title_score, length_score,
            dbs_score, sbs_score,
            position_score, keyword_score, total_score):
        self.text = str(text)
        self.index = int(index)
        self.of = int(of)
        self.title_score = float(title_score)
        self.length_score = float(length_score)
        self.dbs_score = float(dbs_score)
        self.sbs_score = float(sbs_score)
        self.position_score = float(position_score)
        self.keyword_score = float(keyword_score)
        self.total_score = float(total_score)

    def __init__(
            self, text, index, of,
            title_score, length_score,
            dbs_score, sbs_score):
        # (str, int, int, float, float, float, float) -> None
        position_score = score_position(
            index, of)
        keyword_score = score_keyword_frequency(
            dbs_score, sbs_score)
        total_score = score_total(
            title_score, keyword_score, length_score, position_score)

        self._init_(
            text, index, of,
            title_score, length_score,
            dbs_score, sbs_score,
            position_score, keyword_score, total_score)

    def __str__(self):
        return self.text

    def __repr__(self):
        return self._repr_(
            self.text,
            self.index,
            self.of,
            self.title_score,
            self.length_score,
            self.dbs_score,
            self.sbs_score)

    def __eq__(self, other):
        return roughly.eq(self.total_score, other.total_score)

    def __lt__(self, other):
        return roughly.lt(self.total_score, other.total_score)

    def __gt__(self, other):
        return roughly.gt(self.total_score, other.total_score)

    def __ne__(self, other):
        return roughly.ne(self.total_score, other.total_score)

    def __ge__(self, other):
        return roughly.ge(self.total_score, other.total_score)

    def __le__(self, other):
        return roughly.le(self.total_score, other.total_score)
