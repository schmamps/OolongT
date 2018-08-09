"""Mock ScoredKeyword """
import typing

from oolongt.typedefs.scored_keyword import (KEYWORD_SCORE_K, ScoredKeyword,
                                             score_keyword)


class SampleKeyword(ScoredKeyword):
    def __init__(self, pairs: typing.Dict, of: int) -> None:
        """Initialize

        Arguments:
            pairs {typing.Dict} -- `{'word': word, 'count': instances of word}`
            of {int} -- total number of words

        Returns:
            None -- SampleKeyword
        """
        self.word = pairs.get('word', 'foo')                    # type: str
        self.count = pairs.get('count', 1)                      # type: int
        self.of = of                                            # type: int
        self.score = (
            pairs.get('score', score_keyword(self.count, of)))  # type: float

    @classmethod
    # pylint: disable=undefined-variable
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
