"""Content extractor for HTML files"""
import typing

from bs4 import BeautifulSoup

from oolongt.simple_io import read_file
from oolongt.typedefs import Content


def get_doc(path: str) -> BeautifulSoup:
    html = read_file(path)
    doc = BeautifulSoup(html, features='html.parser')

    return doc


def load(path: str) -> typing.Tuple:
    doc = get_doc(path)
    body = doc.get_text('\n')
    title = doc.title.string
    keywords = []  # type: typing.List[str]

    return body, title, keywords


def parse(path: str) -> Content:
    return Content(load, path)
