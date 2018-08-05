"""Mock ScoredSentence"""
from oolongt.constants import COMPOSITE_TOLERANCE
from oolongt.typing.scored_sentence import ScoredSentence

from oolongt import roughly


def auto_id(index, of):
    pad = len(str(of))
    template = '{{0:{0}d}} of {{1}}'.format(pad)
    return template.format(index + 1, of)


class SampleSentence(ScoredSentence):
    def __init__(self, data_dict, of):
        # type: (dict, int) -> None
        text = data_dict.get('text', '')
        index = data_dict.get('index', 0)
        title_score = data_dict.get('title_score', 0)
        length_score = data_dict.get('length_score', 0)
        dbs_score = data_dict.get('dbs_score', 0)
        sbs_score = data_dict.get('sbs_score', 0)
        position_score = data_dict.get('position_score', 0)
        keyword_score = data_dict.get('keyword_score', 0)
        total_score = data_dict.get('total_score', 0)

        self.rank = data_dict.get('rank', 0)
        self._init_(
            text, index, of,
            title_score, length_score,
            dbs_score, sbs_score, keyword_score,
            position_score, total_score)
        self.id = data_dict.get('id', auto_id(index, of))

    def __eq__(self, other):
        # type: (SampleSentence, ScoredSentence) -> bool
        if (self.text != other.text):
            return False

        if (self.index != other.index):
            return False

        if (self.of != other.of):
            return False

        if roughly.ne(self.title_score, other.title_score,
                      rel_tol=COMPOSITE_TOLERANCE):
                return False

        if roughly.ne(self.length_score, other.length_score,
                      rel_tol=COMPOSITE_TOLERANCE):
            return False

        if roughly.ne(self.dbs_score, other.dbs_score,
                      rel_tol=COMPOSITE_TOLERANCE):
            return False

        if roughly.ne(self.sbs_score, other.sbs_score,
                      rel_tol=COMPOSITE_TOLERANCE):
            return False

        if roughly.ne(self.position_score, other.position_score):
            return False

        if roughly.ne(self.keyword_score, other.keyword_score,
                      rel_tol=COMPOSITE_TOLERANCE):
            return False

        if roughly.ne(self.total_score, other.total_score,
                      rel_tol=COMPOSITE_TOLERANCE):
            return False

        return True

    def equals(self, other):
        """Compare SampleSentence to ScoredSentence in correct order

        Arguments:
            other {ScoredSentence} -- ScoredSentence received

        Returns:
            bool -- all properties match
        """
        # type: (SampleSentence, ScoredSentence) -> bool
        return self == other
