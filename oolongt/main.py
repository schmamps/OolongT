from .nodash import pluck, sort_by
from .summarizer import Summarizer

DEFAULT_SORT_KEY = 'order'
DEFAULT_REVERSE = False
DEFAULT_LENGTH = 5


def score_sentences(title, text, source=None, category=None):
    """List every sentence, sorted by total score

    Arguments:
        title {str} -- title of content
        text {str} -- body of content

    Keyword Arguments:
        source {any} -- unused (default: {None})
        category {any} -- unused (default: {None})

    Returns:
        List[Dict] -- List of sentences with scoring and metadata
    """
    summarizer = Summarizer()
    sentences = summarizer.get_sentences(text, title, source, category)

    return sentences


def summarize(title, text,
              length=DEFAULT_LENGTH,
              sort_key=DEFAULT_SORT_KEY, reverse=DEFAULT_REVERSE,
              source=None, category=None):
    """Get top sentences in the specified order

    Where length >= 1, length is an absolute number of sentences
    Where length  < 1, length is a fraction of the total sentence count

    Arguments:
        title {str} -- title of content
        text {str} -- body of content

    Keyword Arguments:
        length {int or float < 1} -- lines to return (int) or
            fraction of total (float) (default: {5})
        order_by {str} -- sort sentences by specified key
            (default: {'order'})
        asc {bool} -- ASCending order (default: {True})
        source {any} -- unused (default: {None})
        category {any} -- unused (default: {None})

    Returns:
        list[str] -- top sentences sorted by criteria
    """
    sentences = sort_by(
        score_sentences(title, text, source, category),
        ['total_score', 'order'], reverse=True)
    slice_length = get_slice_length(length, len(sentences))

    ordered = sort_by(
        sentences[:slice_length], sort_key, reverse=reverse)

    return pluck(ordered, 'text')


def get_slice_length(nominal, total):
    """Determine how many sentences to return

    Arguments:
        nominal {int, float} -- fraction of total/absolute number to return
        total {int} -- total number of sentences to return

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
        return int(nominal * total)

    return max([1, int(nominal)])
