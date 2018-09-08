"""Parse HTML documents"""
from bs4.element import Tag

from ..io import get_contents
from ..typedef import OPT_STR, PATH_STR
from ..ugly_soup import UglyQuery, UglySoup
from .text_document import TextDocument


def process(html: str) -> UglySoup:
    """Parse and reduce noise in `html`

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


def get_source(path: PATH_STR) -> UglySoup:
    """Load HTML from `path`

    Arguments:
        path {str} -- local/remote path to HTML

    Returns:
        UglySoup -- BeautifulSoup
    """
    html = get_contents(path)
    src = process(html)

    return src


def get_body(src: UglySoup) -> str:
    """Get document body content

    Arguments:
        src {UglySoup} -- BeautifulSoup

    Returns:
        str -- best match for content
    """
    body = src.query_sequence(
        UglyQuery('main'),
        UglyQuery('article'),
        UglyQuery('body'))

    return body


def get_og_title(tag: Tag) -> OPT_STR:
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
    open_graph = UglyQuery('meta', get_og_title)
    title_tag = UglyQuery('title')

    title = src.query_sequence(open_graph, title_tag)

    return title


class HtmlDocument(TextDocument):
    """Parse HTML"""
    def __init__(self, path: PATH_STR) -> None:
        """Initialize

        Arguments:
            path {str} -- path to HTML
        """
        src = get_source(path)
        body = get_body(src)
        title = get_title(src)

        self._initialize_document(body, title, path)

    @staticmethod
    def supports(path: OPT_STR, ext: OPT_STR) -> bool:
        path_str = str(path)[:4]

        return path_str in ['http', 'ftp:'] or str(ext).startswith('htm')
