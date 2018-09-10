"""Simple I/O helpers"""
import typing
from json import JSONDecodeError, loads
from pathlib import Path
from re import findall
from urllib import request

from ..constants import PKG_NAME, VERSION
from ..pipe import pipe
from ..typings import PathOrString


def is_supported_scheme(path: str) -> bool:
    """Claim support for scheme in path

    Arguments:
        path {str} -- path to file

    Returns:
        bool -- scheme is supported
    """
    return len(findall(r'^(file|ftp|https*):', path)) > 0


def get_user_agent() -> str:
    """Get User-Agent header value

    Returns:
        str -- browser UA
    """
    platform = 'Cross-Platform'

    return 'Mozilla/5.0 ({}) {}/{}'.format(platform, PKG_NAME, VERSION)


def build_request(path: str):
    """Convert path to URL request

    Arguments:
        path {str} -- path to document
    """
    headers = {'User-Agent': get_user_agent()}
    req = request.Request(path, headers=headers)

    return req


def get_absolute_path(path: str) -> str:
    """Get absolute path to file

    Arguments:
        path {str} -- path to file

    Returns:
        str -- absolute path to file
    """
    abs_path = Path(path).absolute()

    return str(abs_path)


def get_local_url(path: str) -> str:
    """Covert local path to URL

    Arguments:
        path {str} -- path to file

    Returns:
        str -- URL to file
    """
    url = 'file:' + request.pathname2url(path)

    return url


def get_stream(path: PathOrString) -> typing.IO[typing.Any]:
    """Stream read file at `path`

    Arguments:
        path {PathOrString} -- str or pathlib.Path

    Keyword Arguments:
        binary {bool} -- read as binary (default: {False})

    Returns:
        typing.IO[typing.Any] -- io.TextIO or io.BufferedIOBase
    """
    path_str = str(path)

    if is_supported_scheme(path_str):
        pipes = [build_request]

    else:
        pipes = [get_absolute_path, get_local_url]

    return pipe(path_str, pipes, request.urlopen)


def get_contents(path: PathOrString, binary=False) -> typing.Any:
    """Read file at `path` into string

    Arguments:
            path {PathOrString} -- path to file

    Returns:
        str -- contents of file
    """
    with get_stream(path) as stream:
        contents = stream.read()  # type: bytes

    return contents if binary else contents.decode('utf-8')


def read_file(path: PathOrString) -> str:
    """Load text from file at `path`

    Arguments:
            path {PathOrString} -- path to file

    Returns:
            str -- text in file
    """
    try:
        contents = get_contents(path)

    except (IOError, NotADirectoryError) as err:
        raise IOError(str(err))

    return contents


def load_json(path: typing.Any) -> typing.Dict:
    """Load JSON from file at `path`

    Arguments:
            path {PathOrString} -- path to file

    Returns:
            dict -- data in file
    """
    try:
        contents = read_file(path)

    except IOError:
        raise JSONDecodeError('I/O error reading file', path, 0)

    return loads(contents)
