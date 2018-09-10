"""Base class for content"""
import re
import typing
from unicodedata import normalize

from ..constants import BUILTIN, DEFAULT_IDIOM, DEFAULT_LENGTH
from ..pipe import pipe
from ..repr_able import ReprAble
from ..summarizer import ScoredSentence
from ..text import summarize, score_body_sentences
from ..typings import StringList


def strip_strs(str_list: typing.Iterable[typing.Any]) -> StringList:
    """Strip whitespace around strings

    Arguments:
        str_list {typing.List[str]} -- list of strings

    Returns:
        typing.List[str] -- trimmed strings
    """
    items = [str(item).strip() for item in str_list]

    return [item for item in items if len(item) > 0]


def split_strs(text: typing.Any, sep: str = r'\s+') -> StringList:
    """Split `text` by separator `sep`

    Arguments:
        text {str} -- text to split

    Keyword Arguments:
        sep {str} -- string to split on (default: {' '})

    Returns:
        StringList -- list of split strings
    """
    subject = str(text) if text and text is not True else ''

    return re.split(sep, subject)


def join_strs(words: StringList, sep: str = ' ') -> str:
    """Join list `words` by string `sep`

    Arguments:
        words {StringList} -- list of words

    Returns:
        str -- joined words
    """
    return sep.join(words)


def norm_text(spec: typing.Any) -> str:
    """Get text (empty string if false-y)

    Returns:
        str -- input in tidy string
    """
    norm = pipe(spec, split_strs, strip_strs, join_strs)

    return norm


def encode_ascii(text: str) -> str:
    """Get low-value character representation of string

    Arguments:
        text {str} -- UTF-8 encoded string

    Returns:
        str -- string with low value characters
    """
    return normalize('NFKD', text).encode('ascii', 'ignore').decode('utf8')


# pylint: disable=no-self-use,unused-argument
class Content(ReprAble):
    """Base class for content"""
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

    def _initialize_content(self, body: typing.Any, title: typing.Any):
        """Initialize basic properties

        Arguments:
            body {typing.Any} -- nominal content body
            title {typing.Any} -- nominal content title
        """
        self._body = norm_text(body)
        self._title = norm_text(title)

    def __init__(self, body: typing.Any, title: typing.Any) -> None:
        """Initialize basic properties

        Arguments:
            body {typing.Any} -- nominal content body
            title {typing.Any} -- nominal content title
        """
        self._initialize_content(body, title)

    def score_sentences(
            self,
            root: str = BUILTIN,
            idiom: str = DEFAULT_IDIOM) -> typing.List[ScoredSentence]:
        """List and score every sentence in `self.body`

        Keyword Arguments:
            root {str} -- root directory of idiom config
            idiom {str} -- basename of idiom config

        Returns:
            typing.List[ScoredSentence] --
                List of sentences with scoring and metadata
        """
        return score_body_sentences(self.body, self.title, root, idiom)

    def summarize(
            self,
            limit: float = DEFAULT_LENGTH,
            root: str = BUILTIN,
            idiom: str = DEFAULT_IDIOM) -> StringList:
        """Get `limit` best sentences from `body` in content order

        See documentation for oolongt.text.summarize()

        Keyword Arguments:
            limit {float} -- limit of sentences to return (see text package)
            root {str} -- root directory of idiom data
                (default: {parser.BUILTIN})
            idiom {str} -- basename of idiom file
                (default: {parser.DEFAULT_IDIOM})

        Returns:
            StringList -- top sentences in content order
        """
        return summarize(self.body, self.title, limit, root, idiom)

    def __str__(self) -> str:
        return self.body

    def __repr__(self) -> str:
        return self._repr_(self._body, self._title)
