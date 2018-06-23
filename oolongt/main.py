"""Simple sentence scoring & summarization functions"""
from . import parser
from .nodash import pluck, sort_by
from .summarizer import Summarizer

DEFAULT_SORT_KEY = 'order'
DEFAULT_REVERSE = False
DEFAULT_LENGTH = 5


def score_sentences(title, text,
                    root=parser.BUILTIN, lang=parser.DEFAULT_LANG,
                    source=None, category=None):
    # type: (str, str, str, str, any, any) -> list[dict]
    """List and score every sentence in `text`

    Arguments:
        title {str} -- title of content
        text {str} -- body of content

    Keyword Arguments:
        root {str} -- root directory of language config
        lang {str} -- basename of language config
        source {any} -- unused (default: {None})
        category {any} -- unused (default: {None})

    Returns:
        list[dict] -- List of sentences with scoring and metadata
    """
    summarizer = Summarizer()
    sentences = summarizer.get_sentences(text, title, source, category)

    return sentences


def summarize(title, text,
              length=DEFAULT_LENGTH,
              sort_key=DEFAULT_SORT_KEY, reverse=DEFAULT_REVERSE,
              root=parser.BUILTIN, lang=parser.DEFAULT_LANG,
              source=None, category=None):
    # type: (str, str, int, str, bool, str, str, any, any) -> list[dict]
    """Get `length` sentences from `text` sorted by `sort_key`

    Where length >= 1, length is an absolute number of sentences
    Where length  < 1, length is a fraction of the total sentence count

    Arguments:
        title {str} -- title of content
        text {str} -- body of content

    Keyword Arguments:
        length {int or float < 1} -- lines to return (int) or
            fraction of total (float) (default: {5})
        sort_key {str} -- sort sentences by specified key
            (default: {'order'})
        reverse {bool} -- descending order (default: {False})
        source {any} -- unused (default: {None})
        category {any} -- unused (default: {None})

    Returns:
        list[str] -- top sentences sorted by criteria
    """
    sentences = sort_by(
        score_sentences(title, text, root, lang, source, category),
        ['total_score', 'order'],
        reverse=True)
    slice_length = get_slice_length(length, len(sentences))

    ordered = sort_by(
        sentences[:slice_length], sort_key, reverse=reverse)

    return pluck(ordered, 'text')


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
