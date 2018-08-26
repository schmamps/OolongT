import re
import typing
from pathlib import Path
from unicodedata import normalize

from .repr_able import ReprAble


def strip_strs(str_list: typing.List[str]) -> typing.List[str]:
    """Strip whitespace around strings

    Arguments:
        str_list {typing.List[str]} -- list of strings

    Returns:
        typing.List[str] -- trimmed strings
    """
    return [item.strip() for item in str_list]


def get_body(doc_data: typing.Dict[str, typing.Any]) -> str:
    """Get content body (empty string if false-y)

    Returns:
        str -- content body
    """
    return str(doc_data.get('body') or '').strip()


def create_title(path: str) -> str:
    """Auto-generate a content title from filename

    Arguments:
        path {str} -- path to file

    Returns:
        str -- content title
    """
    file_path = Path(path)

    stem = normalize(
        'NFKD', file_path.stem).encode('ascii', 'ignore').decode('utf8')
    words = strip_strs(re.split(r'[,_\-\.\s]+', stem, flags=re.IGNORECASE))

    return ' '.join(words).title()


def get_title(doc_data: typing.Dict[str, typing.Any], path: str) -> str:
    """Get title property from document loader

    Arguments:
        doc_data {typing.Dict[str, typing.Any]} -- document data
        path {str} -- path to file

    Returns:
        str -- best-available value for document title
    """
    return doc_data.get('title') or create_title(path)


def get_keywords(doc_data: typing.Dict[str, typing.Any]):
    """Generate list of keywords from document data

    Arguments:
        doc_data {typing.Dict[str, typing.Any]} -- document data

    Returns:
        typing.List[str] -- list of keywords
    """
    kw_spec = doc_data.get('keywords') or ''
    kws = kw_spec if isinstance(kw_spec, list) else kw_spec.split(',')

    return strip_strs(kws)


class Content(ReprAble):
    def __init__(self, load_func: typing.Callable, path: str) -> None:
        doc_data = load_func(path)

        self.load_func = load_func.__name__
        self.path = path
        self.body = get_body(doc_data)
        self.title = get_title(doc_data, path)
        self.keywords = get_keywords(doc_data)

    def __repr__(self):
        return self._repr_(self.load_func, self.path)

    def __str__(self):
        return self.body
