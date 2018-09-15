"""Simple sentence scoring & summarization functions"""
import typing

from .. import BUILTIN, DEFAULT_IDIOM, DEFAULT_LENGTH
from ..pipe import pipe
from ..summarizer import ScoredSentence, Summarizer
from ..typings import StringList

ScoredSentenceList = typing.List[ScoredSentence]


def score_body_sentences(
        body: str,
        title: str,
        root: str = BUILTIN,
        idiom: str = DEFAULT_IDIOM) -> ScoredSentenceList:
    """List and score every sentence in `body`

    Arguments:
        body {str} -- body of content
        title {str} -- title of content

    Keyword Arguments:
        root {str} -- root directory of idiom config
        idiom {str} -- basename of idiom config

    Returns:
        typing.List[ScoredSentence] --
            List of sentences with scoring and metadata
    """
    summarizer = Summarizer(root, idiom)
    sentences = summarizer.get_all_sentences(body, title)

    return sentences


def sort_sentences_by_score(
        sentences: ScoredSentenceList) -> ScoredSentenceList:
    """Sort sentences by score

    Arguments:
        sentences {ScoredSentenceList} -- list of sentences

    Returns:
        ScoredSentenceList -- sorted list
    """
    return sorted(sentences, reverse=True)


def dedupe_sentences(sentences: ScoredSentenceList) -> ScoredSentenceList:
    """Remove duplicate sentences

    Arguments:
        sentences {ScoredSentenceList} -- all scored sentences
        slice_len {int} -- max number of sentences to return

    Returns:
        ScoredSentenceList -- de-duplicated sentences
    """
    texts = []  # type: typing.List[str]
    unique = []  # type: ScoredSentenceList

    for sent in sentences:
        if sent.text not in texts:
            texts.append(sent.text)
            unique.append(sent)

    return unique


def get_slice_length(nominal: float, total: int) -> int:
    """Calculate actual number of sentences to return

    Arguments:
        nominal {float} -- fraction of total/absolute number to return
        of {int} -- total number of sentences in body

    Raises:
        ValueError -- invalid length argument

    Returns:
        int -- number of sentences to return
    """
    slice_len = nominal

    if nominal <= 0:
        raise ValueError('Invalid summary length: ' + str(nominal))

    if nominal < 1:
        slice_len = nominal * total

    return round(min(slice_len, total))


def get_best_sentences(
        body: str,
        title: str,
        limit: float = DEFAULT_LENGTH,
        root: str = BUILTIN,
        idiom: str = DEFAULT_IDIOM) -> ScoredSentenceList:
    """Get best unique sentences from `body` in score order, qty: `limit`

    Arguments:
        body {str} -- body of content
        title {str} -- title of content

    Keyword Arguments:
        limit {float} -- # of sentences (default: {DEFAULT_LENGTH})
        root {str} -- root directory of idiom data
            (default: {Parser.BUILTIN})
        idiom {str} -- basename of idiom file
            (default: {parser.DEFAULT_IDIOM})

    Returns:
        list[ScoredSentence] -- best sentences from source text
    """
    sentences = pipe(
        score_body_sentences(body, title, root, idiom),
        sort_sentences_by_score,
        dedupe_sentences)
    slice_len = get_slice_length(limit, len(sentences))

    return sentences[:slice_len]


def summarize(
        body: str,
        title: str,
        limit: float = DEFAULT_LENGTH,
        root: str = BUILTIN,
        idiom: str = DEFAULT_IDIOM) -> StringList:
    """Get `limit` best sentences from `body` in content order

    if `limit` < 1:
        len(return) = int(limit * len(sentences))
    else:
        len(return) = min(limit, len(sentences))

    Arguments:
        body {str} -- body of content
        title {str} -- title of content

    Keyword Arguments:
        limit {float} -- sentences to return (int) or
            fraction of total (float) (default: {DEFAULT_LENGTH})
        root {str} -- root directory of idiom data
            (default: {parser.BUILTIN})
        idiom {str} -- basename of idiom file
            (default: {parser.DEFAULT_IDIOM})

    Returns:
        StringList -- top sentences in content order
    """
    sentences = get_best_sentences(body, title, limit, root, idiom)

    return [s.text for s in sorted(sentences, key=lambda x: x.index)]
