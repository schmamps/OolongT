from pytest import mark
from src.oolongt.parser import ScoredKeyword
from tests.helpers import pad_to_longest


def gen_scored_keyword(count: int, total: int, word: str = 'spam'):
    """Generate instance of ScoredKeyword

    Arguments:
        count {int} -- instances of `word`
        total {int} -- total number of words in text

    Keyword Arguments:
        word {str} -- word property of ScoredKeyword (default: {'spam'})

    Returns:
        ScoredKeyword -- scored keyword
    """
    return ScoredKeyword(word, count, total)


def parametrize_words():
    """Parametrize word tests

    Returns:
        typing.List[tuple] -- test parameters
    """
    return mark.parametrize(
        'word,count,total',
        [('ham', 1, 1), ('spam', 1, 1), ('eggs', 1, 1), ('bacon', 1, 1), ],
        ids=pad_to_longest(['ham', 'spam', 'eggs', 'bacon']))
