import typing

from bs4.element import Tag

from .text_document import TextDocument
from .ugly_soup import UglySoup as BeautifulSoup
from .ugly_query import UglyQuery


QUERY_RESULT = typing.Union[str, None]


def process(html: str) -> BeautifulSoup:
    soup = BeautifulSoup(html, features='html.parser')
    ignore_tags = [
        'script',
        'noscript',
        'style',
        'img', ]

    for tag in soup(ignore_tags):
        tag.decompose()

    return soup


def get_body(src: BeautifulSoup) -> str:
    """Get document body content

    Arguments:
        src {BeautifulSoup} -- [description]
        path {str} -- [description]

    Returns:
        str -- [description]
    """
    queries = (
        UglyQuery('main'),
        UglyQuery('article'),
        UglyQuery('body'), )
    body = src.query_sequence(queries)

    return body


def get_og_title(tag: Tag) -> QUERY_RESULT:
    """Get OpenGraph-based title

    Arguments:
        tag {Tag} -- page element

    Returns:
        QUERY_DATA -- str or None
    """
    if tag.get('property') == 'og:title':
        return tag.get('content')

    return None


def get_title(src: BeautifulSoup) -> str:
    queries = (
        UglyQuery('meta', get_og_title),
        UglyQuery('title'), )
    title = src.query_sequence(queries)

    return title


def get_keywords(src: BeautifulSoup) -> typing.List[str]:
    return []


class HtmlDocument(TextDocument):
    def get_source(self, path: str):
        html = super().get_source(path)
        src = process(html)

        return src

    def __init__(self, path: str) -> None:
        src = self.get_source(path)

        body = get_body(src)
        title = get_title(src)
        keywords = None

        super().__init__(body, title, keywords, path)

    @staticmethod
    def supports(path: str, ext: str) -> bool:
        return path.startswith('http') or ext.startswith('htm')
