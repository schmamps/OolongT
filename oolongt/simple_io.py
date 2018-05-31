""" Quick and dirty JSON loader """

from io import open as io_open
from json import loads
from sys import version_info


def load_json(path):
    """Load data from the specified path

    Arguments:
            path {str} -- path to file

    Returns:
            Dict -- data in file
    """
    contents = read_file(path)

    return loads(contents)


def read_file(path):
    """Load text from the specified path

    Arguments:
            path {str} -- path to file

    Returns:
            str -- text in file
    """
    contents = ''

    with io_open(path, 'r', encoding='utf-8') as file:
        contents = file.read()

    if version_info < (3, 0):
        contents = contents.encode('ascii', 'ignore')

    return contents
