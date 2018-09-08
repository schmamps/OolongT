"""Quick and dirty file readers"""
import typing
from json import loads, JSONDecodeError
from pathlib import Path
from re import findall
from urllib import request


def load_json(path: typing.Any) -> typing.Dict:
    """Load JSON from file at `path`

    Arguments:
            path {typing.Any} -- path to file

    Returns:
            dict -- data in file
    """
    try:
        contents = read_file(path)

    except IOError:
        raise JSONDecodeError('I/O error reading file', path, 0)

    return loads(contents)


def is_url(path: str):
    return len(findall(r'^(file|ftp|https*):', path)) > 0


def get_local_url(path: str) -> str:
    abs_path = str(Path(path).absolute())
    url = 'file:' + request.pathname2url(abs_path)

    return url


def get_file_url(path: str) -> str:
    url = path if is_url(path) else get_local_url(path)

    return url


def get_stream(path: typing.Any) -> typing.IO[typing.Any]:
    """Stream read file at `path`

    Arguments:
        path {typing.Any} -- str or pathlib.Path

    Keyword Arguments:
        binary {bool} -- read as binary (default: {False})

    Returns:
        typing.IO[typing.Any] -- io.TextIO or io.BufferedIOBase
    """
    url = get_file_url(str(path))
    stream = request.urlopen(url)

    return stream


def get_contents(path: typing.Any, binary=False) -> typing.Any:
    """Read file at `path` into string

    Arguments:
            path {typing.Any} -- path to file

    Returns:
        str -- contents of file
    """

    with get_stream(path) as stream:
        contents = stream.read()  # type: bytes

    return contents if binary else contents.decode('utf-8')


def read_file(path: typing.Any) -> str:
    """Load text from file at `path`

    Arguments:
            path {typing.Any} -- path to file

    Returns:
            str -- text in file
    """
    try:
        contents = get_contents(path)

    except (IOError, NotADirectoryError) as e:
        raise IOError(str(e))

    return contents
