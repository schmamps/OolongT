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


def get_path_forms(path: PathOrString) -> typing.Tuple[Path, str]:
    """Get nominal path as instance of pathlib.Path and str

    Arguments:
        path {PathOrString} -- path to document

    Returns:
        typing.Tuple[Path, str] -- Path object and path as string
    """
    path_str = str(path)
    path_obj = path if isinstance(path, Path) else Path(path_str)

    return path_obj, path_str


def get_path_url(path: PathOrString) -> str:
    """Covert local path to URL

    Arguments:
        path {str} -- path to file

    Returns:
        str -- URL to file
    """
    path_obj, path_str = get_path_forms(path)

    if is_supported_scheme(path_str):
        return build_request(path_str)

    return path_obj.absolute().as_uri()


def get_stream(path: PathOrString) -> typing.IO[typing.Any]:
    """Stream read file at `path`

    Arguments:
        path {PathOrString} -- str or pathlib.Path

    Keyword Arguments:
        binary {bool} -- read as binary (default: {False})

    Returns:
        typing.IO[typing.Any] -- io.TextIO or io.BufferedIOBase
    """
    return pipe(path, get_path_url, request.urlopen)


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

    # pylint: disable=broad-except
    except (IOError, NotADirectoryError) as err:
        raise IOError(str(err))
    # pylint: enable=broad-except

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
