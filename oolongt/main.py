"""Simple sentence scoring & summarization functions"""
import typing

from oolongt.constants import BUILTIN, DEFAULT_LANG, DEFAULT_LENGTH
from oolongt.parser import Parser
from oolongt.summarizer import Summarizer
from oolongt.typedefs import ScoredSentence


def score_body_sentences(
        body: str,
        title: str,
        root: str = BUILTIN,
        lang: str = DEFAULT_LANG,
        source: typing.Any = None,
        category: typing.Any = None
        ) -> typing.List[ScoredSentence]:
    """List and score every sentence in `body`

    Arguments:
        body {str} -- body of content
        title {str} -- title of content

    Keyword Arguments:
        root {str} -- root directory of language config
        lang {str} -- basename of language config
        source {any} -- unused (default: {None})
        category {any} -- unused (default: {None})

    Returns:
        typing.List[ScoredSentence] --
            List of sentences with scoring and metadata
    """
    summarizer = Summarizer()
    sentences = summarizer.get_all_sentences(body, title, source, category)

    return sentences


def get_slice_length(nominal: typing.Any, of: int) -> int:
    """Calculate actual number of sentences to return

    Arguments:
        nominal {float or int} -- fraction of total/absolute number to return
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
        length: typing.Any = DEFAULT_LENGTH,
        root: str = BUILTIN,
        lang: str = DEFAULT_LANG,
        source: typing.Any = None,
        category: typing.Any = None
        ) -> typing.List[ScoredSentence]:
    """Get best sentences from `body` in score order, qty: `length`

    Arguments:
        body {str} -- body of content
        title {str} -- title of content

    Keyword Arguments:
        length {int or float} -- # of sentences (default: {DEFAULT_LENGTH})
        root {str} -- root directory of language data
            (default: {parser.BUILTIN})
        lang {str} -- basename of language file
            (default: {parser.DEFAULT_LANG})
        source {any} -- unused (default: {None})
        category {any} -- unused (default: {None})

    Returns:
        list[ScoredSentence] -- best sentences from source text
    """
    sentences = score_body_sentences(
        body, title, root, lang, source, category)
    slice_length = get_slice_length(length, len(sentences))

    return sorted(sentences, reverse=True)[:slice_length]


def summarize(
        body: str,
        title: str,
        length: typing.Any = DEFAULT_LENGTH,
        root: typing.Any = BUILTIN,
        lang: str = DEFAULT_LANG,
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
        length {int or float < 1} -- sentences to return (int) or
            fraction of total (float) (default: {5})
        root {str} -- root directory of language data
            (default: {parser.BUILTIN})
        lang {str} -- basename of language file
            (default: {parser.DEFAULT_LANG})
        source {any} -- unused (default: {None})
        category {any} -- unused (default: {None})

    Returns:
        list[str] -- top sentences in content order
    """
    sentences = get_best_sentences(
        title, body, length, root, lang, source, category)

    return [s.text for s in sorted(sentences, key=lambda x: x.index)]
