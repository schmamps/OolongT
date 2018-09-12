"""Test `ParserConfig`"""
import typing
from pathlib import Path

from pytest import mark

from src.oolongt import BUILTIN, DEFAULT_IDIOM
from src.oolongt.parser.parser_config import (
    ParserConfig, get_config_path, get_stop_words, load_idiom, parse_config)
from tests.constants import IDIOM_PATH
from tests.helpers import assert_ex, check_exception, pad_to_longest

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


@mark.parametrize(
    'root,idiom,expected',
    [(IDIOM_PATH, TEST_IDIOM_NAME, TEST_IDIOM_JSON), ],
    ids=pad_to_longest(['test path', ]))
def test_get_config_path(root: str, idiom: str, expected: Path) -> None:
    """Test `get_config_path` for ParserConfig

    Arguments:
        root {str} -- root directory of idiom config
        idiom {str} -- basename of idiom config
        expected {Path} -- self explanatory
    """
    received = get_config_path(root, idiom)

    assert (received == expected), assert_ex(
        'config path',
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
        ({'nltk': True, 'user': ['foo']}, -10), ],
    ids=pad_to_longest([
        'nltk: default, user: default',
        'nltk: False,   user: default',
        'nltk: True,    user: default',
        'nltk: default, user: 0',
        'nltk: default, user: 1',
        'nltk: False,   user: 0',
        'nltk: False,   user: 1',
        'nltk: True,    user: 0',
        'nltk: True,    user: 1', ]))
def test_get_stop_words(
        spec: typing.Dict[str, typing.Any],
        expected: int) -> None:
    """Test `get_stop_words` for ParserConfig

    Arguments:
        spec {typing.Dict[str, typing.Any]} -- nominal configuration
        expected {int} -- number of expected words (-ish)
    """
    idiom_spec = {'stop_words': spec}
    language = 'english'
    user = spec.get('user', [])

    received = list(get_stop_words(idiom_spec, language))
    missing = len([x for x in user if x not in received]) if user else 0
    test = (missing == 0)

    if test:
        if expected < 0:
            test = (len(received) > abs(expected))

        else:
            test = (len(received) == expected)

    assert test, assert_ex(
        'get stop words',
        received,
        expected)


@mark.parametrize(
    'path_dict,expected', [
        ({}, DEFAULT_IDIOM_EXPECTED),
        ({'idiom': 'default'}, DEFAULT_IDIOM_EXPECTED),
        ({'root': BUILTIN}, DEFAULT_IDIOM_EXPECTED),
        ({
            'idiom': TEST_IDIOM_NAME,
            'root': IDIOM_PATH
        }, TEST_IDIOM_EXPECTED),
        ({'idiom': 'malformed', 'root': IDIOM_PATH}, ValueError),
        ({'idiom': 'INVALID', 'root': IDIOM_PATH}, ValueError), ],
    ids=pad_to_longest([
        'root: def., idiom: def.      == default idiom',
        'root: def., idiom: exp.      == default idiom',
        'root: exp., idiom: def.      == default idiom',
        'root: exp., idiom: exp.      == default idiom',
        'root: exp., idiom: MALFORMED == (error)',
        'root: exp., idiom: INVALID   == (error)', ]))
def test_parse_config(
        path_dict: typing.Dict[str, typing.Any],
        expected: typing.Any) -> None:
    """Parse a nominal configuration

    Arguments:
        path_dict {typing.Dict[str, typing.Any]} --
            arguments for Parser initialization
        expected {typing.Any} -- idiom config or exception
    """
    path_kwargs = {'root': BUILTIN, 'idiom': DEFAULT_IDIOM}
    path_kwargs.update(path_dict)
    cfg_path = get_config_path(**path_kwargs)

    try:
        ideal, language, stop_words = parse_config(cfg_path)
        received = (ideal, language, len(stop_words))

    except Exception as err:  # pylint: disable=broad-except
        received = check_exception(err, expected)

    assert (received == expected), assert_ex(
        'parse config',
        received,
        expected)


@mark.parametrize(
    'kwargs,expected',
    [
        ({}, DEFAULT_IDIOM_EXPECTED),
        ({'idiom': '../../../etc'}, PermissionError),
        ({'root': Path(__file__)}, FileNotFoundError),
        ({'idiom': 'malformed', 'root': IDIOM_PATH}, ValueError), ],
    ids=pad_to_longest([
        'valid: yes',
        'valid: no, traversal',
        'valid: no, file not found',
        'valid: no, parse error', ]))
def test_load_idiom(
        kwargs: typing.Dict[str, typing.Any],
        expected: typing.Tuple[int, str, int]) -> None:
    """Test `load_idiom` for ParserConfig

    Arguments:
        kwargs {typing.Dict[str, typing.Any]} -- kwargs passed to Parser
        expected {typing.Tuple[int, str, int]} -- expected data
    """
    test = False

    try:
        received = load_idiom(**kwargs)
        test = compare_loaded_idiom(received, expected)

    # pylint: disable=broad-except
    except (PermissionError, FileNotFoundError, ValueError) as err:
        test = check_exception(err, expected) is not None
    # pylint: enable=broad-except

    assert test, assert_ex('config', received, expected)


# pylint: disable=too-few-public-methods,no-self-use
class TestParserConfig:
    """Test `ParserConfig`"""
    @mark.parametrize(
        'root,idiom,expected',
        [(BUILTIN, DEFAULT_IDIOM, DEFAULT_IDIOM_EXPECTED), ],
        ids=pad_to_longest(['defaults', ]))
    def test___init__(
            self,
            root: str,
            idiom: str,
            expected: typing.Tuple[int, str, int]) -> None:
        """Test `ParserConfig` initialization

        Arguments:
        root {str} -- root directory of idiom config
        idiom {str} -- basename of idiom config
            expected {typing.Tuple[int, str, int]} --
                [ideal words, NLTK language, stop word count]
        """
        config = ParserConfig(root, idiom)
        received = (
            config.ideal_sentence_length,
            config.language,
            len(config.stop_words))

        assert (received == expected), assert_ex(
            'parser config',
            received,
            expected)
