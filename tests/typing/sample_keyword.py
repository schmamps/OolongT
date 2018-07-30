"""Mock ScoredKeyword """
from oolongt.typing.scored_keyword import (
    score_keyword, ScoredKeyword, KEYWORD_SCORE_K)


class SampleKeyword(ScoredKeyword):
    def __init__(self, pairs, of):
        self.word = pairs.get('word', 'foo')
        self.count = pairs.get('count', 1)
        self.of = of
        self.score = pairs.get('score', score_keyword(self.count, of))

    @classmethod
    def by_score(cls, score, count=1):
        # type: (float, int) -> SampleKeyword
        """When you don't need a fancy ScoredKeyword

        Arguments:
            score {float} -- keyword score

        Keyword Arguments:
            count {int} -- number of appearances (default: {1})

        Returns:
            SampleKeyword -- sample keyword with specified score, count
        """
        return cls({'score': score, 'count': count}, 1)
