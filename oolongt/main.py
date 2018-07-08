"""Simple sentence scoring & summarization functions"""
from . import parser
from .summarizer import Summarizer


DEFAULT_LENGTH = 5


def score_body_sentences(body, title,
                         root=parser.BUILTIN, lang=parser.DEFAULT_LANG,
                         source=None, category=None):
    # type: (str, str, str, str, any, any) -> list[ScoredSentence]
    """List and score every sentence in `text`

    Arguments:
        body {str} -- body of content
        title {str} -- title of content

    Keyword Arguments:
        root {str} -- root directory of language config
        lang {str} -- basename of language config
        source {any} -- unused (default: {None})
        category {any} -- unused (default: {None})

    Returns:
        list[ScoredSentence] -- List of sentences with scoring and metadata
    """
    summarizer = Summarizer()
    sentences = summarizer.get_sentences(body, title, source, category)

    return sentences


def get_slice_length(nominal, of):
    # type: (float, int) -> int
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


def get_best_sentences(body, title,
                       length=DEFAULT_LENGTH,
                       root=parser.BUILTIN, lang=parser.DEFAULT_LANG,
                       source=None, category=None):
    # type: (str, str, int, str, str, any, any) -> list[ScoredSentence]
    """Get best sentences from `body` in score order, qty: `length`

    Arguments:
        body {str} -- body of content
        title {str} -- title of content

    Keyword Arguments:
        length {int or float} -- # of sentences (default: {DEFAULT_LENGTH})
        root {str} -- root dir for language data (default: {parser.BUILTIN})
        lang {str} -- basename of lang file (default: {parser.DEFAULT_LANG})
        source {any} -- unused (default: {None})
        category {any} -- unused (default: {None})

    Returns:
        list[ScoredSentence] -- best sentences from source text
    """
    sentences = score_body_sentences(
        body, title, root, lang, source, category)
    slice_length = get_slice_length(length, len(sentences))

    return sorted(sentences, reverse=True)[:slice_length]


def summarize(body, title,
              length=DEFAULT_LENGTH,
              root=parser.BUILTIN, lang=parser.DEFAULT_LANG,
              source=None, category=None):
    # type: (str, str, int, str, str, any, any) -> list[str]
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
        source {any} -- unused (default: {None})
        category {any} -- unused (default: {None})

    Returns:
        list[str] -- top sentences in content order
    """
    sentences = get_best_sentences(
        title, body, length, root, lang, source, category)

    return [s.text for s in sorted(sentences, key=lambda x: x.index)]
