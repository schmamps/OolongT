"""Content extractor for HTML files"""
import typing

from bs4 import BeautifulSoup

from oolongt.simple_io import read_file
from oolongt.typedefs import Content


def get_doc(path: str) -> BeautifulSoup:
    """Get BeautifulSoup document at `path`

    Arguments:
        path {str} -- path to document (local)

    Returns:
        BeautifulSoup -- document
    """
    html = read_file(path)
    doc = BeautifulSoup(html, features='html.parser')

    return doc


def get_keywords(  # pylint: disable=unused-argument
        doc: BeautifulSoup) -> typing.List[str]:
    """Get keywords (if any)

    Arguments:
        doc {BeautifulSoup} -- HTML document

    Returns:
        typing.List[str] -- document keywords
    """
    # pylint: disable=fixme
    # TODO: get /html/head/meta[name=keywords]
    return []


def load(path: str) -> typing.Tuple:
    """Load HTML and extract properties

    Arguments:
        path {str} -- path to document

    Returns:
        typing.Dict[str, typing.Any] -- {body: str, title: str, keywords: Any}
    """
    doc = get_doc(path)
    body = doc.get_text('\n')
    title = doc.title.string
    keywords = get_keywords(doc)

    return body, title, keywords


def parse(path: str) -> Content:
    """Get content of document at `path`

    Arguments:
        path {str} -- path to document

    Returns:
        Content -- text properties of document
    """
    return Content(load, path)
