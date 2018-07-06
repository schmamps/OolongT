

from oolongt.typing.scored_keyword import (
    score_keyword, ScoredKeyword, SCORE_K)


class SampleKeyword(ScoredKeyword):
    def __init__(self, pairs, of):
        self.word = pairs.get('word', 'foo')
        self.count = pairs.get('count', 1)
        self.of = of
        self.score = pairs.get('score', score_keyword(self.count, of))

    @classmethod
    def by_score(cls, score, count=1):
        return cls({'score': score, 'count': count}, 1)
