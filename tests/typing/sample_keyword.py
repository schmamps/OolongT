

from oolongt.typing.scored_keyword import ScoredKeyword, SCORE_K


class SampleKeyword(ScoredKeyword):
    def __init__(self, pairs):
        self.word = pairs.get('word', 'foo')
        self.score = pairs.get('total_score', 0)
        self.count = pairs.get('count', 0)

    @classmethod
    def by_score(cls, score, count=0):
        return cls({'total_score': score, 'count': count})
