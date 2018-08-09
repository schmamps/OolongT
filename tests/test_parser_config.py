import typing
from json import JSONDecodeError
from pathlib import Path

from pytest import mark

from oolongt.constants import (BUILTIN, DEFAULT_LANG, DEFAULT_NLTK_STOPS,
                               DEFAULT_USER_STOPS)
from oolongt.typedefs.parser_config import (ParserConfig, get_config_paths,
                                            get_stop_words, load_language,
                                            parse_config)
from tests.helpers import assert_ex, check_exception, pad_to_longest

BASE_LANG_PATH = Path(__file__).parent.joinpath('lang')
TEST_LANG_NAME = 'valid'
TEST_LANG_JSON = BASE_LANG_PATH.joinpath(TEST_LANG_NAME + '.json')
TEST_LANG_EXPECTED = (2, 'valid', 2)
DEFAULT_LANG_EXPECTED = (20, 'english', 179)
TEST_DEFAULT_INITIAL = False
TEST_DEFAULT_CUSTOM = ['foo', 'bar']
TEST_DEFAULT_STOPS = {
    'nltk': TEST_DEFAULT_INITIAL,
    'custom': TEST_DEFAULT_CUSTOM, }


def compare_loaded_language(
        received: typing.Tuple[int, str, typing.List],
        expected: typing.Tuple[int, str, int]
        ) -> bool:
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
    [(BASE_LANG_PATH, TEST_LANG_NAME, TEST_LANG_JSON), ],
    ids=['test path', ])
def test_get_config_paths(root: str, lang: str, expected_path: Path) -> None:
    """Get config paths

    Arguments:
        root {str} -- root directory of language config
        lang {str} -- basename of language config
        expected_path {Path} -- self explanatory
    """
    expected = (expected_path, BASE_LANG_PATH)
    received = get_config_paths(root, lang)

    assert (received == expected), assert_ex(
        'config paths',
        received,
        expected)


@mark.parametrize(
    'spec,expected',
    [
        ({}, -1,),
        ({'nltk': False}, 0),
        ({'nltk': True}, -10),
        ({'user': []}, -10),
        ({'user': ['foo']}, -10),
        ({'nltk': False, 'user': []}, 0),
        ({'nltk': False, 'user': ['foo']}, 1),
        ({'nltk': True, 'user': []}, -10),
        ({'nltk': True, 'user': ['foo']}, -10),
    ],
    ids=pad_to_longest([
        'nltk: default, user: default',
        'nltk: False,   user: default',
        'nltk: True,    user: default',
        'nltk: default, user: 0',
        'nltk: default, user: 1',
        'nltk: False,   user: 0',
        'nltk: False,   user: 1',
        'nltk: True,    user: 0',
        'nltk: True,    user: 1',
    ]))
def test_get_stop_words(spec: typing.Dict, expected: int) -> None:
    """Get stop words

    Arguments:
        spec {typing.Dict} -- nominal configuration
        expected {int} -- number of expected words (-ish)
    """
    lang_spec = {'stop_words': spec}
    nltk_language = 'english'
    user = spec.get('user', [])

    received = list(get_stop_words(lang_spec, nltk_language))
    missing = len([x for x in user if x not in received]) if user else 0
    test = (missing == 0)

    if test:
        if (expected < 0):
            test = (len(received) > abs(expected))

        else:
            test = (len(received) == expected)

    assert test, assert_ex(
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
        ({'lang': 'INVALID', 'root': BASE_LANG_PATH}, ValueError),
    ],
    ids=pad_to_longest([
        'root: def., lang: def.      == default lang',
        'root: def., lang: exp.      == default lang',
        'root: exp., lang: def.      == default lang',
        'root: exp., lang: exp.      == default lang',
        'root: exp., lang: MALFORMED == (error)',
        'root: exp., lang: INVALID   == (error)',
    ]))
def test_parse_config(path_dict: typing.Dict, expected: typing.Any) -> None:
    """Parse a nominal configuration

    Arguments:
        path_dict {typing.Dict} -- arguments for Parser initialization
        expected {typing.Any} -- language config or exception
    """
    path_kwargs = {'root': BUILTIN, 'lang': DEFAULT_LANG}
    path_kwargs.update(path_dict)
    cfg_path, _ = get_config_paths(**path_kwargs)

    try:
        ideal, nltk_language, stop_words = parse_config(str(cfg_path))
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
    ids=pad_to_longest([
        'valid: yes',
        'valid: no, traversal',
        'valid: no, file not found',
        'valid: no, parse error',
    ]))
def test_load_language(
        kwargs: typing.Dict,
        expected: typing.Tuple[int, str, int]
        ) -> None:
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
        [(BUILTIN, DEFAULT_LANG, DEFAULT_LANG_EXPECTED), ],
        ids=pad_to_longest(['defaults', ])
    )
    def test_init(
            self,
            root: str,
            lang: str,
            expected: typing.Tuple[int, str, int]
            ) -> None:
        """Test initialization

        Arguments:
        root {str} -- root directory of language config
        lang {str} -- basename of language config
            expected {typing.Tuple[int, str, int]} --
                [ideal words, NLTK language, stop word count]
        """
        config = ParserConfig(root, lang)
        received = (
            config.ideal_sentence_length,
            config.nltk_language,
            len(config.stop_words))

        assert (received == expected), assert_ex(
            'parser config',
            received,
            expected)
