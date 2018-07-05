from oolongt.typing.scored_sentence import ScoredSentence
from tests import helpers


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
            dbs_score, sbs_score,
            position_score, keyword_score, total_score)

    def __eq__(self, other):
        # type: (SampleSentence, ScoredSentence) -> bool
        if (self.text != other.text):
            return False

        if (self.index != other.index):
            return False

        if (self.of != other.of):
            return False

        if self.title_score != helpers.roughly(other.title_score):
            return False

        if self.length_score != helpers.roughly(other.length_score):
            return False

        if self.dbs_score != helpers.roughly(other.dbs_score):
            return False

        if self.sbs_score != helpers.roughly(other.sbs_score):
            return False

        if self.position_score != helpers.roughly(other.position_score):
            return False

        if self.keyword_score != helpers.roughly(other.keyword_score):
            return False

        if self.total_score != helpers.roughly(other.total_score):
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
