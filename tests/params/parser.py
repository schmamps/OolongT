"""Parser testing params"""
import typing
from pathlib import Path

from src.oolongt.constants import BUILTIN, DEFAULT_IDIOM, KEYWORD_SCORE_K
from src.oolongt.parser import ScoredKeyword
from tests.constants import IDIOM_PATH, SAMPLES
from tests.params.helpers import parametrize
from tests.params.summarizer import get_sample_ids, get_samples

TEST_IDIOM_NAME = 'valid'
TEST_IDIOM_JSON = IDIOM_PATH.joinpath(TEST_IDIOM_NAME + '.json')
TEST_IDIOM_EXPECTED = (2, 'valid', 2)
DEFAULT_IDIOM_EXPECTED = (20, 'english', 201)
TEST_DEFAULT_INITIAL = False
TEST_DEFAULT_CUSTOM = ['foo', 'bar']
TEST_DEFAULT_STOPS = {
    'nltk': TEST_DEFAULT_INITIAL,
    'custom': TEST_DEFAULT_CUSTOM, }


def compare_loaded_idiom(
        received: typing.Tuple[int, str, typing.List],
        expected: typing.Tuple[int, str, int]) -> bool:
    """Compare loaded idiom data to expected

    Arguments:
        received {dict} -- received data
        expected {dict} -- expected data

    Raises:
        ValueError -- Wrong data
    """
    # ideal_sentence_length, idiom
    for i in range(2):
        if received[i] != expected[i]:
            raise ValueError('wrong idiom data loaded')

    # stop_words
    if len(received[2]) != expected[2]:
        raise ValueError('stop word mismatch')

    return True


def gen_sk_inst(count: int, total: int, word: str = 'spam'):
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


def param_get_config_path():
    """Parametrize `test_get_config_path`"""
    names = 'root,idiom,expected'
    vals = ((IDIOM_PATH, TEST_IDIOM_NAME, TEST_IDIOM_JSON), )
    ids = ('test path', )

    return parametrize(names, vals, ids)


def param_get_stop_words():
    """Parametrize `test_get_stop_words`"""
    names = 'spec,expected'
    vals = (
        ({}, -1,),
        ({'nltk': False}, 0),
        ({'nltk': True}, -10),
        ({'user': []}, -10),
        ({'user': ['foo']}, -10),
        ({'nltk': False, 'user': []}, 0),
        ({'nltk': False, 'user': ['foo']}, 1),
        ({'nltk': True, 'user': []}, -10),
        ({'nltk': True, 'user': ['foo']}, -10),
    )
    ids = (
        'nltk: default, user: default',
        'nltk: False,   user: default',
        'nltk: True,    user: default',
        'nltk: default, user: 0',
        'nltk: default, user: 1',
        'nltk: False,   user: 0',
        'nltk: False,   user: 1',
        'nltk: True,    user: 0',
        'nltk: True,    user: 1',
    )

    return parametrize(names, vals, ids)


def param_parse_config():
    """Parametrize `test_parse_config`"""
    names = 'path_dict,expected'
    vals = (
        ({}, DEFAULT_IDIOM_EXPECTED),
        ({'idiom': 'default'}, DEFAULT_IDIOM_EXPECTED),
        ({'root': BUILTIN}, DEFAULT_IDIOM_EXPECTED),
        ({
            'idiom': TEST_IDIOM_NAME,
            'root': IDIOM_PATH
        }, TEST_IDIOM_EXPECTED),
        ({'idiom': 'malformed', 'root': IDIOM_PATH}, ValueError),
        ({'idiom': 'INVALID', 'root': IDIOM_PATH}, ValueError),
    )
    ids = (
        'root: def., idiom: def.      == default idiom',
        'root: def., idiom: exp.      == default idiom',
        'root: exp., idiom: def.      == default idiom',
        'root: exp., idiom: exp.      == default idiom',
        'root: exp., idiom: MALFORMED == (error)',
        'root: exp., idiom: INVALID   == (error)',
    )

    return parametrize(names, vals, ids)


def param_load_idiom():
    """Parametrize `test_load_idiom`"""
    names = 'kwargs,expected'
    vals = (
        ({}, DEFAULT_IDIOM_EXPECTED),
        ({'idiom': '../../../etc'}, PermissionError),
        ({'root': Path(__file__)}, FileNotFoundError),
        ({'idiom': 'malformed', 'root': IDIOM_PATH}, ValueError),
    )
    ids = (
        'valid: yes',
        'valid: no, traversal',
        'valid: no, file not found',
        'valid: no, parse error',
    )

    return parametrize(names, vals, ids)


def param_parser_config_init():
    """Parametrize ParserConfig init"""
    names = 'root,idiom,expected'
    vals = ((BUILTIN, DEFAULT_IDIOM, DEFAULT_IDIOM_EXPECTED), )
    ids = ('defaults', )

    return parametrize(names, vals, ids)


def param_remove_punctuations():
    """Parametrize `test_remove_punctuations`"""
    names = 'samp'
    vals = get_samples(('empty', 'sentence_1word', 'sentence_list', ))
    ids = ('empty string', 'one word', 'list of sentences', )

    return parametrize(names, vals, ids)


def param_get_all_words():
    """Parametrize `test_get_all_words`"""
    names = 'samp'
    vals = get_samples(('sentence_1word', 'sentence_overlong'))
    ids = ('one ', 'a long sentence')

    return parametrize(names, vals, ids)


def param_get_keywords():
    """Parametrize `test_get_keywords`"""
    names = 'samp'
    vals = get_samples(('empty', 'essay_snark'))
    ids = ('empty_string', 'snark_essay')

    return parametrize(names, vals, ids)


def param_split_sentences():
    """Parametrize `test_split_sentences`"""
    names = 'samp'
    vals = get_samples(['sentence_short', 'sentence_list', ] + SAMPLES)
    ids = get_sample_ids(['sentence_short', 'sentence_list', ] + SAMPLES)

    return parametrize(names, vals, ids)


def param_split_words():
    """Parametrize `test_split_words`"""
    names = 'samp'
    vals = get_samples(('empty', 'sentence_1word', 'sentence_medium'))
    ids = ('empty_string', 'one_word', 'medium_sent',)

    return parametrize(names, vals, ids)


def param_score_keyword():
    """Parametrize `test_score_keyword`"""
    names = 'count,total,expected'
    vals = (
        (1, 1, KEYWORD_SCORE_K),
        (-1, 1, ValueError),
        (1, 0, ValueError),
        (2, 1, ValueError),
    )
    ids = ('normal', 'sub0', 'div0/neg', 'overmax', )

    return parametrize(names, vals, ids)


def param_compare_score():
    """Parametrize `test_compare_score`"""
    names = 'score_a,score_b,expected'
    vals = (
        (0.0, 1.0, -1),
        (0.999999999999999999, 1.0, 0),
        (1.000000000000000000, 1.0, 0),
        (1.000000000000000001, 1.0, 0),
        (2, 1.0, 1),
    )
    ids = (
        'quite_lt',
        'lt_but_eq',
        'exact_eq',
        'gt_but_eq',
        'quite_gt',
    )

    return parametrize(names, vals, ids)


def param_compare_word():
    """Parametrize `test_compare_word`"""
    names = 'word_a,word_b,expected'
    vals = (('spal', 'spam', -1), ('spam', 'spam', 0), ('span', 'spam', 1))
    ids = ('lt', 'eq', 'gt')

    return parametrize(names, vals, ids)


def param_compare_keywords():
    """Parametrize `test_compare_keywords`"""
    names = 'kw_a,kw_b,is_lt,is_eq,reason'
    vals = (
        (gen_sk_inst(1, 2), gen_sk_inst(1, 1), True, False, 's'),
        (gen_sk_inst(1, 2), gen_sk_inst(1, 2), False, True, 's'),
        (gen_sk_inst(1, 2), gen_sk_inst(1, 3), False, False, 's'),
        (gen_sk_inst(1, 2, 'ham'), gen_sk_inst(1, 2), True, False, 'l'),
        (gen_sk_inst(1, 2, 'eggs'), gen_sk_inst(1, 2), True, False, 'l'),
        (gen_sk_inst(1, 2, 'bacon'), gen_sk_inst(1, 2), False, False, 'l'),
        (gen_sk_inst(1, 2, 'spal'), gen_sk_inst(1, 2), True, False, 'w'),
        (gen_sk_inst(1, 2, 'spam'), gen_sk_inst(1, 2), False, True, 'w'),
        (gen_sk_inst(1, 2, 'span'), gen_sk_inst(1, 2), False, False, 'w'),
    )
    ids = (
        'score-lt_b',
        'score-eq_b',
        'score-gt_b',
        'length-lt_b',
        'length-eq_b',
        'length-gt_b',
        'string-lt_b',
        'string-eq_b',
        'string-gt_b',
    )

    return parametrize(names, vals, ids)


def parametrize_words():
    """Parametrize word tests

    Returns:
        typing.List[tuple] -- test parameters
    """
    names = 'word,count,total'
    vals = (('ham', 1, 1), ('spam', 1, 1), ('eggs', 1, 1), ('bacon', 1, 1), )
    ids = ('ham', 'spam', 'eggs', 'bacon')

    return parametrize(names, vals, ids)
