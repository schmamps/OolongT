"""Simple sentence scoring & summarization functions"""
import typing

from oolongt.constants import BUILTIN, DEFAULT_IDIOM, DEFAULT_LENGTH
from oolongt.parser import Parser
from oolongt.summarizer import Summarizer
from oolongt.typedefs.scored_sentence import ScoredSentence


def score_body_sentences(
        body: str,
        title: str,
        root: str = BUILTIN,
        idiom: str = DEFAULT_IDIOM,
        source: typing.Any = None,
        category: typing.Any = None,
        length: typing.Any = None
        ) -> typing.List[ScoredSentence]:
    """List and score every sentence in `body`

    Arguments:
        body {str} -- body of content
        title {str} -- title of content

    Keyword Arguments:
        root {str} -- root directory of idiom config
        idiom {str} -- basename of idiom config
        source {any} -- unused (default: {None})
        category {any} -- unused (default: {None})

    Returns:
        typing.List[ScoredSentence] --
            List of sentences with scoring and metadata
    """
    summarizer = Summarizer()
    sentences = summarizer.get_all_sentences(body, title, source, category)

    return sentences


def get_slice_length(nominal: float, of: int) -> int:
    """Calculate actual number of sentences to return

    Arguments:
        nominal {float} -- fraction of total/absolute number to return
        of {int} -- total number of sentences in body

    Raises:
        ValueError -- invalid length argument

    Returns:
        int -- number of sentences to return

    >>> get_slice_length(20, 1000)
    20
    >>> get_slice_length(.1, 1000)
    100
    """
    if nominal <= 0:
        raise ValueError('Invalid summary length: ' + str(nominal))

    if nominal < 1:
        return max([1, int(nominal * of)])

    return min([int(nominal), of])


def get_best_sentences(
        body: str,
        title: str,
        length: float = DEFAULT_LENGTH,
        root: str = BUILTIN,
        idiom: str = DEFAULT_IDIOM,
        source: typing.Any = None,
        category: typing.Any = None
        ) -> typing.List[ScoredSentence]:
    """Get best sentences from `body` in score order, qty: `length`

    Arguments:
        body {str} -- body of content
        title {str} -- title of content

    Keyword Arguments:
        length {float} -- # of sentences (default: {DEFAULT_LENGTH})
        root {str} -- root directory of idiom data
            (default: {Parser.BUILTIN})
        idiom {str} -- basename of idiom file
            (default: {parser.DEFAULT_IDIOM})
        source {any} -- unused (default: {None})
        category {any} -- unused (default: {None})

    Returns:
        list[ScoredSentence] -- best sentences from source text
    """
    sentences = score_body_sentences(
        body, title, root, idiom, source, category)
    slice_length = get_slice_length(length, len(sentences))

    return sorted(sentences, reverse=True)[:slice_length]


def summarize(
        body: str,
        title: str,
        length: float = DEFAULT_LENGTH,
        root: str = BUILTIN,
        idiom: str = DEFAULT_IDIOM,
        source: typing.Any = None,
        category: typing.Any = None
        ) -> typing.List[str]:
    """Get `length` best sentences from `body` in content order

    if `length` < 1:
        len(return) = int(length * len(sentences))
    else:
        len(return) = min(length, len(sentences))

    Arguments:
        body {str} -- body of content
        title {str} -- title of content

    Keyword Arguments:
        length {float} -- sentences to return (int) or
            fraction of total (float) (default: {5})
        root {str} -- root directory of idiom data
            (default: {parser.BUILTIN})
        idiom {str} -- basename of idiom file
            (default: {parser.DEFAULT_IDIOM})
        source {any} -- unused (default: {None})
        category {any} -- unused (default: {None})

    Returns:
        list[str] -- top sentences in content order
    """
    sentences = get_best_sentences(
        title, body, length, root, idiom, source, category)

    return [s.text for s in sorted(sentences, key=lambda x: x.index)]
