"""Sample ScoredSentence"""
import typing

import kinda

from src.oolongt.constants import COMPOSITE_TOLERANCE
from src.oolongt.summarizer import ScoredSentence


def auto_id(index: int, total: int) -> str:
    """Generate ID property for sentence

    Arguments:
        index {int} -- sentence index in content
        total {int} -- total number of sentences in content

    Returns:
        str -- sentence id
    """
    pad = len(str(total))
    template = '{{0:{0}d}} of {{1}}'.format(pad)
    return template.format(index + 1, total)


def is_different(sent_a: ScoredSentence, sent_b: ScoredSentence, prop: str):
    """Compare `prop` of `sent_a` to `sent_b`

    Arguments:
        sent_a {ScoredSentence} -- sentence A
        sent_b {ScoredSentence} -- sentence B
        prop {str} -- name of property
    """
    val_a = getattr(sent_a, prop)
    val_b = getattr(sent_b, prop)

    return kinda.ne(val_a, val_b, COMPOSITE_TOLERANCE)


# pylint: disable=super-init-not-called
class SampleSentence(ScoredSentence):
    """Sample ScoredSentence"""
    def __init__(
            self,
            data_dict: typing.Dict[str, typing.Any],
            total: int) -> None:
        """Initialize

        Arguments:
            data_dict {typing.Dict[str, typing.Any]} -- JSON data
            of {int} -- total number of sentences

        Returns:
            SampleSentence -- sample sentence
        """
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
            text, index, total,
            title_score, length_score,
            dbs_score, sbs_score, keyword_score,
            position_score, total_score)
        self.id = str(data_dict.get('id', auto_id(index, total)))  # noqa  pylint: disable=line-too-long,invalid-name

    # pylint: disable=too-many-return-statements
    def __eq__(self, other: ScoredSentence) -> bool:
        """Compare equality

        Arguments:
            other {ScoredSentence} -- scored sentence

        Returns:
            bool -- sentences are equal
        """

        if self.text != other.text:
            return False

        if self.index != other.index:
            return False

        if self.of != other.of:
            return False

        prop_keys = [
            'title', 'length', 'dbs', 'sbs', 'position', 'keyword', 'total']

        for key in prop_keys:
            if is_different(self, other, key + '_score'):
                return False

        return True

    # pylint: enable=too-many-return-statements
    def equals(self, other) -> bool:
        """Compare SampleSentence to ScoredSentence in correct order

        Arguments:
            other {ScoredSentence} -- ScoredSentence received

        Returns:
            bool -- all properties match
        """
        return self == other
