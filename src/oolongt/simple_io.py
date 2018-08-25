"""Quick and dirty file readers"""
import typing
from io import open as io_open
from json import loads, JSONDecodeError


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


def _get_contents(path: typing.Any) -> str:
    """Read file at `path` into string

    Arguments:
            path {typing.Any} -- path to file

    Returns:
        str -- contents of file
    """
    with io_open(str(path), 'r', encoding='utf-8') as fp:
        contents = fp.read()
        fp.close()

    return contents


def read_file(path: typing.Any) -> str:
    """Load text from file at `path`

    Arguments:
            path {typing.Any} -- path to file

    Returns:
            str -- text in file
    """
    try:
        contents = _get_contents(path)

    except (IOError, NotADirectoryError) as e:
        raise IOError(str(e))

    return contents
