"""Base class for content"""
import abc
import re
import typing
from pathlib import Path
from unicodedata import normalize

from ..pipe import pipe
from ..typedefs import NONE_STR, STR_LIST
from ..typedefs.repr_able import ReprAble


def strip_strs(str_list: typing.Iterable[str]) -> STR_LIST:
    """Strip whitespace around strings

    Arguments:
        str_list {typing.List[str]} -- list of strings

    Returns:
        typing.List[str] -- trimmed strings
    """
    items = [item.strip() for item in str_list]

    return [item for item in items if len(item) > 0]


def norm_body(body: typing.Any) -> str:
    """Get content body (empty string if false-y)

    Returns:
        str -- content body
    """
    return str(body).strip() if body else ''


def get_path_stem(path: str) -> str:
    """Convert a path into a string suitable for titles

    Arguments:
        path {str} -- path to document

    Returns:
        str -- filename (minus extension, accents, etc.)
    """
    file_path = Path(path)
    stem = normalize(
        'NFKD', file_path.stem).encode('ascii', 'ignore').decode('utf8')

    return stem


def split_stem(stem: str) -> STR_LIST:
    """Split string into words on CamelCase and other punctuation

    Arguments:
        stem {str} -- stem of filename

    Returns:
        typing.List[str] -- list of words in stem
    """
    words = re.split(
        r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|[,\.\-\s]+', stem)

    return words


def is_mixed(word: str) -> bool:
    """Determine if word is mixed/upper case

    Arguments:
        word {str} -- word

    Returns:
        bool -- is mixed/upper case
    """
    tail = word[1:]
    return (word == word.upper) or (tail != tail.lower())


def entitle(words: typing.List[str]) -> STR_LIST:
    """Convert string to pretty title case

    Arguments:
        words {typing.List[str]} -- list of words

    Returns:
        typing.List[str] -- title-cased words
    """
    entitled = [word if is_mixed(word) else word.title() for word in words]

    return entitled


def norm_title(title: typing.Any, path: NONE_STR) -> str:
    """Get title property from document loader

    Arguments:
        doc_data {typing.Dict[str, typing.Any]} -- document data
        path {str} -- path to file

    Returns:
        str -- best-available value for document title
    """
    words = title.split() if title else pipe(path, get_path_stem, split_stem)
    words = pipe(words, strip_strs, entitle)

    return ' '.join(words)


def norm_keywords(keywords: typing.Any) -> STR_LIST:
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


# pylint: disable=no-self-use,unused-argument
class Content(ReprAble):
    """Base class for content"""
    @abc.abstractmethod
    def get_source(self, path: str):
        """Get parser for content

        Arguments:
            path {str} -- path to content

        Returns:
            typing.Any -- content parser
        """
        return path

    def get_body(self, src) -> str:
        """Extract body (if any) in `src`

        Arguments:
            src {typing.Any} -- content source

        Returns:
            str -- content
        """
        return str(src) if src else ''

    def get_title(self, src) -> str:
        """Extract title (if any) in `src`

        Arguments:
            src {typing.Any} -- content source

        Returns:
            str -- title
        """
        return ''

    def get_keywords(self, src) -> typing.Union[str, STR_LIST]:
        """Extract keywords (if any) in `src`

        Arguments:
            src {typing.Any} -- content source

        Returns:
            typing.List[str] -- document keywords
        """
        return []

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
    def keywords(self) -> STR_LIST:
        """Get keywords of content

        Returns:
            str -- content keywords
        """
        return self._keywords

    @property
    def path(self) -> NONE_STR:
        """Get path to document (if any)

        Returns:
            NONE_STR -- path do document
        """
        return self._path if self._path else None

    def __init__(
            self,
            body: typing.Any,
            title: typing.Any,
            keywords: typing.Any,
            path: NONE_STR = None) -> None:
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
        """Claim support for a given path/extension

        Arguments:
            _ {str} -- ignored
            __ {str} -- ignored

        Returns:
            bool -- False
        """
        return False

    def __str__(self) -> str:
        return self.body

    def __repr__(self) -> str:
        return self._repr_(
            self._body,
            self._title,
            self._keywords,
            path=self._path)
