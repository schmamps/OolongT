""" Simple I/O module tests """
import typing
from pathlib import Path

from pytest import mark

from src.oolongt.constants import PKG_NAME, VERSION
from src.oolongt.io.io import (
    build_request, get_absolute_path, get_contents, get_local_url, get_stream,
    get_user_agent, is_supported_scheme, load_json, read_file)
from src.oolongt.typings import PathOrString
from tests.helpers import check_exception, pad_to_longest
from tests.params.io import param_json, param_read

ABSOLUTE_FILE = str(Path(__file__).absolute())


@mark.parametrize(
    'path,expected',
    [
        ('/etc/hosts', False),
        ('file:///etc/hosts', True),
        ('ftp://x', True),
        ('http://x', True),
        ('https://x', True), ],
    ids=pad_to_longest([
        'local',
        'file:',
        'ftp:',
        'http:',
        'https:', ]))
def test_is_supported_scheme(path: PathOrString, expected: bool):
    """Test is_supported_scheme

    Arguments:
        path {PathOrString} -- path to document
        expected {bool} -- scheme is supported
    """
    received = is_supported_scheme(path)

    assert received == expected


@mark.parametrize(
    'val',
    [(PKG_NAME), (VERSION)],
    ids=pad_to_longest(['name', 'version']))
def test_get_user_agent(val: str):
    """Test get_user_agent()

    Arguments:
        val {str} -- string in user agent
    """
    assert val in get_user_agent()


@mark.parametrize(
    'path',
    [('http://localhost/')],
    ids=['localhost'])
def test_build_request(path: PathOrString):
    """Test build_request

    Arguments:
        path {PathOrString} -- path to document
    """
    received = build_request(path)

    assert received.__class__.__name__ == 'Request'


@mark.parametrize(
    'path,expected',
    [(__file__, ABSOLUTE_FILE), (Path(__file__), ABSOLUTE_FILE)],
    ids=pad_to_longest(['str', 'Path']))
def test_get_absolute_path(path: PathOrString, expected: str):
    """Test get_absolute_path

    Arguments:
        path {PathOrString} -- path to document
        expected {str} -- expected string
    """
    received = get_absolute_path(path)

    assert received == expected


@mark.parametrize(
    'path,expected',
    [('/spam/eggs/bacon.ham', 'file:///spam/eggs/bacon.ham')],
    ids=pad_to_longest(['spam']))
def test_get_local_url(path: PathOrString, expected: str):
    """Test get_local_url

    Arguments:
        path {PathOrString} -- path to document
        expected {str} -- expected string
    """
    received = get_local_url(path)

    assert received == expected


@mark.parametrize(
    'path,expected',
    [(__file__, __file__)],
    ids=pad_to_longest(['__file__']))
def test_get_stream(path: PathOrString, expected):
    """Test get_stream

    Arguments:
        path {PathOrString} -- path to document
        expected {[type]} -- TODO:
    """
    with get_stream(path) as stream:
        received = stream.fp.name

    assert received == expected


def _test_read(func: typing.Callable, path: PathOrString, expected) -> bool:
    """Test an I/O reading function

    Arguments:
        func {typing.Callable} -- oolongt.io function
        path {PathOrString} -- path to document
        expected {typing.Any} -- contents of document or exception

    Returns:
        bool -- result is expected
    """
    try:
        received = func(path).strip()

    except Exception as err:  # pylint: disable=broad-except
        received = check_exception(err, expected)

    return received == expected


@param_read()
def test_get_contents(path: PathOrString, expected):
    """Test get_contents()

    Arguments:
        path {PathOrString} -- path to document
        expected {typing.Any} -- contents of document or exception
    """
    assert _test_read(get_contents, path, expected)


@param_read(IOError, IOError)
def test_read_file(path: PathOrString, expected: str):
    """Test read_file

    Arguments:
        path {PathOrString} -- path to document
        expected {typing.Any} -- contents of document or exception
    """
    assert _test_read(read_file, path, expected)


@mark.parametrize(
    'path,expected',
    [
        param_json('valid.json', True),
        param_json('valid.FAIL', False),
        param_json('malformed.json', False), ],
    ids=pad_to_longest(['valid', 'bad_path', 'malformed']))
def test_load_json(path: PathOrString, expected) -> None:
    """Test load_json

    Arguments:
        path {PathOrString} -- path to document
    """
    try:
        received = load_json(path)

    except Exception as err:  # pylint: disable=broad-except
        received = check_exception(err, expected)

    assert received == expected
