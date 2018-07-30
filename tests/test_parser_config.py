from pathlib import Path

from pytest import mark

from oolongt.constants import DEFAULT_LANG, BUILTIN
from oolongt.typing.parser_config import (
    ParserConfig, get_config_paths, get_stop_word_key, get_stop_words,
    load_language, parse_config,
    DEFAULT_INITIAL_STOPS, DEFAULT_CUSTOM_STOPS)
from tests.helpers import assert_ex, check_exception, compare_dict

BASE_LANG_PATH = Path(__file__).parent.joinpath('lang')
TEST_LANG_NAME = 'valid'
TEST_LANG_JSON = BASE_LANG_PATH.joinpath(TEST_LANG_NAME + '.json')
TEST_LANG_EXPECTED = (2, 'valid', 2)
DEFAULT_LANG_EXPECTED = (20, 'english', 398)
TEST_DEFAULT_INITIAL = ['foo']
TEST_DEFAULT_CUSTOM = ['bar']
TEST_DEFAULT_STOPS = {
    'initial': TEST_DEFAULT_INITIAL,
    'custom': TEST_DEFAULT_CUSTOM, }


def compare_loaded_language(received, expected):
    # type: (dict, dict) -> bool
    """Compare loaded language data to expected

    Arguments:
        received {dict} -- received data
        expected {dict} -- expected data

    Raises:
        ValueError -- Wrong data
    """
    # ideal_sentence_length, nltk_language
    for i in range(2):
        if (received[i] != expected[i]):
            raise ValueError('wrong language data loaded')

    # stop_words
    if len(received[2]) != expected[2]:
        raise ValueError('stop word mismatch')

    return True


@mark.parametrize(
    'root,lang,expected_path',
    [
        (BASE_LANG_PATH, TEST_LANG_NAME, TEST_LANG_JSON),
    ],
    ids=[
        'test path'
    ])
def test_get_config_paths(root, lang, expected_path):
    expected = (expected_path, BASE_LANG_PATH)
    received = get_config_paths(root, lang)

    assert (received == expected), assert_ex(
        'config paths',
        received,
        expected)


@mark.parametrize(
    'stop_cfg,key,nltk_language,default_val,min_len,max_len',
    [
        ({'foo': ['bar']}, 'foo', None, ['baz', 'quux'], 1, 1),
        ({}, 'foo', None, ['baz', 'quux'], 2, 2),
        ({'foo': 'nltk'}, 'foo', None, None, 100, 99999),
        ({}, 'foo', None, 'nltk', 100, 99999),
    ],
    ids=[
        'value at key \'foo\'',
        'return default',
        'NLTK (explicit)',
        'NLTK (implicit)',
    ]
)
def test_get_stop_word_key(stop_cfg, key, nltk_language, default_val,
                           min_len, max_len):
    received = len(
        get_stop_word_key(stop_cfg, key, nltk_language, default_val))

    assert(min_len <= received <= max_len), assert_ex(
        'stop word key',
        received,
        ' to '.join([min_len, max_len]))


@mark.parametrize(
    'spec,defaults,expected',
    [
        ({'initial': [], 'custom': []}, TEST_DEFAULT_STOPS, [],),
        (
            {'initial': ['baz'], 'custom': ['quux', 'quuz']},
            TEST_DEFAULT_STOPS,
            ['baz', 'quux', 'quuz'],
        ),
        ({'initial': []}, TEST_DEFAULT_STOPS, TEST_DEFAULT_CUSTOM,),
        ({'custom': []},  TEST_DEFAULT_STOPS, TEST_DEFAULT_INITIAL,),
        ({}, TEST_DEFAULT_STOPS, TEST_DEFAULT_INITIAL + TEST_DEFAULT_CUSTOM,),
    ],
    ids=[
        'exp. initial, exp. custom (empty)',
        'exp. initial, exp. custom (populated)',
        'exp. initial, def. custom (populated)',
        'def. initial, exp. custom (populated)',
        'def. initial, def. custom (populated)',
    ])
def test_get_stop_words(spec, defaults, expected):
    expected = sorted(
        expected)
    received = sorted(list(
        get_stop_words({'stop_words': spec}, None, defaults)))

    assert (received == expected), assert_ex(
        'get stop words',
        received,
        expected)


@mark.parametrize(
    'path_dict,expected', [
        ({}, DEFAULT_LANG_EXPECTED),
        ({'lang': 'en'}, DEFAULT_LANG_EXPECTED),
        ({'root': BUILTIN}, DEFAULT_LANG_EXPECTED),
        ({'lang': TEST_LANG_NAME, 'root': BASE_LANG_PATH}, TEST_LANG_EXPECTED),
        ({'lang': 'malformed', 'root': BASE_LANG_PATH}, ValueError),
        ({'lang': 'INVALID', 'root': BASE_LANG_PATH}, FileNotFoundError),
    ],
    ids=[
        'def. path, def. lang',
        'def. path, exp. lang',
        'exp. path, def. lang',
        'exp. path, exp. lang',
        'invalid language config',
        'missing language config',
    ])
def test_parse_config(path_dict, expected):
    path_kwargs = {'root': BUILTIN, 'lang': DEFAULT_LANG}
    path_kwargs.update(path_dict)
    cfg_path, _ = get_config_paths(**path_kwargs)

    try:
        ideal, nltk_language, stop_words = parse_config(cfg_path)
        received = (ideal, nltk_language, len(stop_words))

    except Exception as e:
        received = check_exception(e, expected)

    assert (received == expected), assert_ex(
        'parse config',
        received,
        expected)


@mark.parametrize(
    'kwargs,expected',
    [
        ({}, DEFAULT_LANG_EXPECTED),
        [{'lang': '../../../etc'}, PermissionError],
        [{'root': Path(__file__)}, FileNotFoundError],
        [{'lang': 'malformed', 'root': BASE_LANG_PATH}, ValueError],
    ],
    ids=[
        'defaults',
        'attempted traversal',
        'file not found',
        'invalid config',
    ])
def test_load_language(kwargs, expected):
    # type: (dict, dict) -> None
    """Test Parser.load_language()

    Arguments:
        kwargs {dict} -- kwargs passed to Parser
        expected {dict} -- expected data
    """
    test = False

    try:
        received = load_language(**kwargs)
        test = compare_loaded_language(received, expected)

    except (PermissionError, FileNotFoundError, ValueError) as e:
        test = check_exception(e, expected) is not None

    assert test, assert_ex('config', received, expected)


class TestParserConfig(object):
    @mark.parametrize(
        'root,lang,expected',
        [(BUILTIN, DEFAULT_LANG, DEFAULT_LANG_EXPECTED)],
        ids=['defaults']
    )
    def test_init(self, root, lang, expected):
        config = ParserConfig(root, lang)
        received = (
            config.ideal_sentence_length,
            config.nltk_language,
            len(config.stop_words))

        assert (received == expected), assert_ex(
            'parser config',
            received,
            expected)
