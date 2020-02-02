"""Sample ScoredKeyword """
import typing

from src.oolongt.parser.scored_keyword import ScoredKeyword, score_keyword


# pylint: disable=super-init-not-called,too-few-public-methods
class SampleKeyword(ScoredKeyword):
    """Sample ScoredKeyword"""
    def __init__(self, pairs: typing.Dict[str, typing.Any], of: int) -> None:
        """Initialize

        Arguments:
            pairs {typing.Dict[str, typing.Any]} --
                `{'word': word, 'count': instances of word}`
            of {int} -- total number of words

        Returns:
            None -- SampleKeyword
        """
        self.word = pairs.get('stem', 'spam')                   # type: str
        self.count = pairs.get('count', 1)                      # type: int
        self.of = of                                            # type: int
        self.score = (
            pairs.get('score', score_keyword(self.count, of)))  # type: float

    @classmethod
    def by_score(cls, score: float, count: int = 1):
        """When you don't need a fancy ScoredKeyword

        Arguments:
            score {float} -- keyword score

        Keyword Arguments:
            count {int} -- number of appearances (default: {1})

        Returns:
            SampleKeyword -- sample keyword with specified score, count
        """
        return cls({'score': score, 'count': count}, 1)
