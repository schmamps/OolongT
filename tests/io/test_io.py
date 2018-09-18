""" Simple I/O module tests """
import typing

from src.oolongt.constants import PKG_NAME, VERSION
from src.oolongt.io.io import (
    build_request, get_contents, get_path_forms, get_path_url, get_stream,
    get_user_agent, is_supported_scheme, load_json, read_file)
from src.oolongt.typings import PathOrString
from tests.helpers import check_exception
from tests.params.helpers import parametrize
from tests.params.io import (
    param_get_path_forms, param_get_path_url, param_load_json, param_read,
    param_scheme)


@param_scheme()
def test_is_supported_scheme(path: PathOrString, expected: bool):
    """Test `is_supported_scheme`

    Arguments:
        path {PathOrString} -- path to document
        expected {bool} -- scheme is supported
    """
    received = is_supported_scheme(path)

    assert received == expected


@parametrize('val', ((PKG_NAME), (VERSION), ), ('name', 'version', ))
def test_get_user_agent(val: str):
    """Test `get_user_agent`

    Arguments:
        val {str} -- string in user agent
    """
    assert val in get_user_agent()


@parametrize('path', [('http://localhost/', )], ('localhost', ))
def test_build_request(path: PathOrString):
    """Test `build_request`

    Arguments:
        path {PathOrString} -- path to document
    """
    received = build_request(path)

    assert received.__class__.__name__ == 'Request'


@param_get_path_forms()
def test_get_path_forms(path: PathOrString, expected: tuple):
    """Test `get_path_forms`

    Arguments:
        path {PathOrString} -- [description]
        expected {tuple} -- [description]
    """
    received = get_path_forms(path)

    assert received == expected


@param_get_path_url()
def test_get_path_url(path: PathOrString, expected: str):
    """Test `get_path_url`

    Arguments:
        path {PathOrString} -- path to document
        expected {str} -- expected string
    """
    spec = get_path_url(path)

    try:
        received = spec.get_full_url()

    except AttributeError:
        received = spec

    assert received == expected


@parametrize('path,expected', ((__file__, __file__), ), ('__file__', ))
def test_get_stream(path: PathOrString, expected):
    """Test `get_stream`

    Arguments:
        path {PathOrString} -- path to document
        expected {[type]} -- stream name
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
    """Test `get_contents`

    Arguments:
        path {PathOrString} -- path to document
        expected {typing.Any} -- contents of document or exception
    """
    assert _test_read(get_contents, path, expected)


@param_read(IOError, IOError)
def test_read_file(path: PathOrString, expected: str):
    """Test `read_file`

    Arguments:
        path {PathOrString} -- path to document
        expected {typing.Any} -- contents of document or exception
    """
    assert _test_read(read_file, path, expected)


@param_load_json()
def test_load_json(path: PathOrString, expected) -> None:
    """Test `load_json`

    Arguments:
        path {PathOrString} -- path to document
    """
    try:
        received = load_json(path)

    except Exception as err:  # pylint: disable=broad-except
        received = check_exception(err, expected)

    assert received == expected
