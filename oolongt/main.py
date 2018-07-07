"""Simple sentence scoring & summarization functions"""
from . import parser
from .summarizer import Summarizer

DEFAULT_SORT_KEY = 'index'
DEFAULT_REVERSE = False
DEFAULT_LENGTH = 5


def score_sentences(title, body,
                    root=parser.BUILTIN, lang=parser.DEFAULT_LANG,
                    source=None, category=None):
    # type: (str, str, str, str, any, any) -> list[dict]
    """List and score every sentence in `text`

    Arguments:
        title {str} -- title of content
        body {str} -- body of content

    Keyword Arguments:
        root {str} -- root directory of language config
        lang {str} -- basename of language config
        source {any} -- unused (default: {None})
        category {any} -- unused (default: {None})

    Returns:
        list[dict] -- List of sentences with scoring and metadata
    """
    summarizer = Summarizer()
    sentences = summarizer.get_sentences(body, title, source, category)

    return sentences


def get_slice_length(nominal, total):
    # type: (float, int) -> int
    """Calculate actual number of sentences to return

    Arguments:
        nominal {float} -- fraction of total/absolute number to return
        total {int} -- total number of sentences to return

    Raises:
        ValueError -- invalid length argument

    Returns:
        str -- number of sentences to return

    >>> get_slice_length(20, 1000)
    20
    >>> get_slice_length(.1, 1000)
    100
    """
    if nominal <= 0:
        raise ValueError('Invalid summary length: ' + str(nominal))

    if nominal < 1:
        return max([1, int(nominal * total)])

    return min([int(nominal), total])


def get_best_sentences(title, body,
                       length=DEFAULT_LENGTH,
                       root=parser.BUILTIN, lang=parser.DEFAULT_LANG,
                       source=None, category=None):
    # type: (str, str, int, str, str, any, any) -> list[ScoredSentence]
    """Get `length` best sentences from `body` in score order

    Returns:
        list[ScoredSentence] -- top sentences from `body`
    """
    sentences = score_sentences(
        title, body, root, lang, source, category)
    slice_length = get_slice_length(length, len(sentences))

    return sorted(sentences, reverse=True)[:slice_length]


def summarize(title, body,
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
        title {str} -- title of content
        body {str} -- body of content

    Keyword Arguments:
        length {int or float < 1} -- sentences to return (int) or
            fraction of total (float) (default: {5})
        source {any} -- unused (default: {None})
        category {any} -- unused (default: {None})

    Returns:
        list[str] -- top sentences sorted by criteria
    """
    sentences = get_best_sentences(
        title, body, length, root, lang, source, category)

    return [s.text for s in sorted(sentences, key=lambda x: x.index)]
