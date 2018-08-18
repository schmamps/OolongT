"""Content extractor for plain text files"""
import typing

from oolongt.simple_io import read_file
from oolongt.typedefs import Content


def load(path: str) -> typing.Tuple:
    body = read_file(path)
    title = False
    keywords = []  # type: typing.List[str]

    return body, title, keywords


def parse(path: str) -> Content:
    return Content(load, path)
