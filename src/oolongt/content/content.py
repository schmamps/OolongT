"""Base class for content"""
import re
import typing

from ..constants import BUILTIN, DEFAULT_IDIOM, DEFAULT_LENGTH
from ..repr_able import ReprAble
from ..summarizer import ScoredSentence
from ..text import score_body_sentences, summarize
from ..typings import StringList


def norm_text(spec: typing.Any) -> str:
    """Get text (empty string if false-y)

    Returns:
        str -- input in tidy string
    """
    return '' if spec is None else re.sub(r'\s+', ' ', str(spec)).strip()


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

    def __init__(self, body: typing.Any, title: typing.Any) -> None:
        """Initialize basic properties

        Arguments:
            body {typing.Any} -- nominal content body
            title {typing.Any} -- nominal content title
        """
        self._body = norm_text(body)
        self._title = norm_text(title)

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
