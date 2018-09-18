"""Test `ParserConfig`"""
import typing
from pathlib import Path

from src.oolongt import BUILTIN, DEFAULT_IDIOM
from src.oolongt.parser.parser_config import (
    ParserConfig, get_config_path, get_stop_words, load_idiom, parse_config)
from tests.helpers import assert_ex, check_exception
from tests.params.parser import (
    compare_loaded_idiom, param_get_config_path, param_get_stop_words,
    param_load_idiom, param_parse_config, param_parser_config_init)


@param_get_config_path()
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


@param_get_stop_words()
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


@param_parse_config()
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


@param_load_idiom()
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
    @param_parser_config_init()
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
