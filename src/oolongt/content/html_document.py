"""Parse HTML documents"""
from bs4.element import Tag

from ..typedefs import NONE_STR
from ..typedefs.ugly_query import UglyQuery
from ..ugly_soup import UglySoup
from .text_document import TextDocument


def process(html: str) -> UglySoup:
    """Parse and filter `html`

    Arguments:
        html {str} -- document HTML

    Returns:
        UglySoup -- BeautifulSoup subclass
    """
    soup = UglySoup(html)
    ignore_tags = [
        'script',
        'noscript',
        'style',
        'img', ]

    for tag in soup(ignore_tags):
        tag.decompose()

    return soup


def get_body(src: UglySoup) -> str:
    """Get document body content

    Arguments:
        src {UglySoup} -- BeautifulSoup

    Returns:
        str -- best match for content
    """
    queries = (
        UglyQuery('main'),
        UglyQuery('article'),
        UglyQuery('body'), )
    body = src.query_sequence(queries)

    return body


def get_og_title(tag: Tag) -> NONE_STR:
    """Get OpenGraph-based title if any, else None

    Arguments:
        tag {Tag} -- page element

    Returns:
        NONE_STR -- str or None
    """
    if tag.get('property') == 'og:title':
        return tag.get('content')

    return None


def get_title(src: UglySoup) -> str:
    """Get title tag string, else empty

    Arguments:
        src {UglySoup} -- BeautifulSoup

    Returns:
        str -- title (if any)
    """
    queries = (
        UglyQuery('meta', get_og_title),
        UglyQuery('title'), )
    title = src.query_sequence(queries)

    return title


class HtmlDocument(TextDocument):
    """Parse HTML"""
    def get_source(self, path: str) -> UglySoup:
        """Load HTML from `path`

        Arguments:
            path {str} -- local/remote path to HTML

        Returns:
            UglySoup -- BeautifulSoup
        """
        html = super().get_source(path)
        src = process(html)

        return src

    def __init__(self, path: str) -> None:
        """Initialize

        Arguments:
            path {str} -- path to HTML
        """
        src = self.get_source(path)

        body = get_body(src)
        title = get_title(src)
        keywords = None

        super().__init__(body, title, keywords, path)

    @staticmethod
    def supports(path: NONE_STR, ext: NONE_STR) -> bool:
        """Register support for given extension (path ignored)

        Arguments:
            path {str} -- path to document
            ext {str} -- extension of document

        Returns:
            bool -- format is supported
        """
        path_str = str(path)[:4]

        return path_str in ['http', 'ftp:'] or str(ext).startswith('htm')
