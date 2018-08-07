"""Quick and dirty file readers"""
from io import open as io_open
from json import loads

from oolongt import PYTHON_2


def load_json(path):
    # type: (str) -> dict
    """Load JSON from file at `path`

    Arguments:
            path {str} -- path to file

    Returns:
            dict -- data in file
    """
    contents = read_file(path)

    return loads(contents)


def _get_contents(path):
    # (str) -> str
    """Read file at `path` into string

    Returns:
        str -- contents of file
    """
    with io_open(str(path), 'r', encoding='utf-8') as fp:
        contents = fp.read()
        fp.close()

        return contents


def read_file(path):
    # type: (str) -> str
    """Load text from file at `path`

    Arguments:
            path {str} -- path to file

    Returns:
            str -- text in file
    """
    contents = _get_contents(path)

    if PYTHON_2:
        contents = contents.encode('ascii', 'ignore').decode('ascii')

    return contents
