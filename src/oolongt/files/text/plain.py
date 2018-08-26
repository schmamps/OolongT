"""Content extractor for plain text files"""
import typing

from oolongt.simple_io import read_file
from oolongt.typedefs import Content


def load(path: str) -> typing.Dict[str, typing.Any]:
    """Read contents of text file as body of content

    Arguments:
        path {str} -- path to file

    Returns:
        typing.Dict[str, typing.Any] -- {'body': ...}
    """
    return {'body': read_file(path)}


def parse(path: str) -> Content:
    return Content(load, path)
