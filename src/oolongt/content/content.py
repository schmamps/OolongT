import abc
import re
import typing
from pathlib import Path
from unicodedata import normalize

from .repr_able import ReprAble


def strip_strs(str_list: typing.Iterable[str]) -> typing.List[str]:
    """Strip whitespace around strings

    Arguments:
        str_list {typing.List[str]} -- list of strings

    Returns:
        typing.List[str] -- trimmed strings
    """
    return [item.strip() for item in str_list]


def norm_body(body: typing.Any) -> str:
    """Get content body (empty string if false-y)

    Returns:
        str -- content body
    """
    return str(body) if body else ''


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


def norm_title(title: typing.Any, path: typing.Union[str, None]) -> str:
    """Get title property from document loader

    Arguments:
        doc_data {typing.Dict[str, typing.Any]} -- document data
        path {str} -- path to file

    Returns:
        str -- best-available value for document title
    """
    if title:
        return str(title)

    return create_title(path) if path else ''


def norm_keywords(keywords: typing.Any) -> typing.List[str]:
    """Generate list of keywords from document data

    Arguments:
        doc_data {typing.Dict[str, typing.Any]} -- document data

    Returns:
        typing.List[str] -- list of keywords
    """
    spec = keywords or ''  # type: typing.Union[typing.Iterable, str]
    is_iter = not isinstance(spec, str) and hasattr(spec, '__iter__')
    kws = set(keywords if is_iter else str(spec).split(','))

    return strip_strs(kws)


class Content(ReprAble):
    @abc.abstractmethod
    def get_source(self, path: str) -> typing.Any:
        pass

    def get_body(self, src) -> str:
        """Extract body (if any) in `src`

        Arguments:
            src {typing.Any} -- content source

        Returns:
            str -- content
        """
        return str(src) if isinstance(src, object) else ''

    def get_title(self, src) -> str:
        """Extract title (if any) in `src`

        Arguments:
            src {typing.Any} -- content source

        Returns:
            str -- title
        """
        return '' if isinstance(src, object) else ''

    def get_keywords(self, src) -> typing.Union[str, typing.List[str]]:
        """Extract keywords (if any) in `src`

        Arguments:
            src {typing.Any} -- content source

        Returns:
            typing.List[str] -- document keywords
        """
        return [] if isinstance(src, object) else ''

    @property
    def body(self) -> str:
        """Get body of content

        Returns:
            str -- content body
        """
        return self._body

    @property
    def title(self) -> str:
        """Get title of content

        Returns:
            str -- content title
        """
        return self._title

    @property
    def keywords(self) -> typing.List[str]:
        """Get keywords of content

        Returns:
            str -- content keywords
        """
        return self._keywords

    @property
    def path(self) -> typing.Union[str, None]:
        return self._path if self._path else None

    def __init__(
            self,
            body: typing.Any,
            title: typing.Any,
            keywords: typing.Any,
            path: typing.Union[str, None] = None) -> None:
        """Initialize

        Arguments:
            body {typing.Any} -- content body
            title {typing.Any} -- content title
            keywords {typing.Any} -- content keywords
            path {str or None} -- path to content

        Returns:
            None
        """
        self._body = norm_body(body)  # type: str
        self._title = norm_title(title, path if path else '')  # type: str
        self._keywords = norm_keywords(keywords)  # type: typing.List[str]
        self._path = path

    @staticmethod
    @abc.abstractmethod
    def supports(_: str, __: str) -> bool:
        pass

    def __str__(self) -> str:
        return self.body

    def __repr__(self) -> str:
        return self._repr_(
            self._body,
            self._title,
            self._keywords,
            path=self._path)
