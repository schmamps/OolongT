from .nodash import pluck, sort_by
from .summarizer import Summarizer


def rank_sentences(title, text,
                   source=None, category=None):
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

    return sort_by(sentences, ['total_score', 'order'])


def summarize(title, text, length=5,
              order_by='order', asc=True,
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
    ranked_list = rank_sentences(title, text, source, category)
    slice_length = get_slice_length(length, len(ranked_list))
    sorted_list = sort_by(
        ranked_list[:slice_length], order_by, not asc)

    return pluck(sorted_list, 'text')


def get_slice_length(nominal, total):
    """Determine how many sentences to return

    Arguments:
        nominal {int, float} -- fraction of total/absolute number to return
        total {int} -- total number of sentences to return

    Raises:
        ValueError -- invalid length argument

    Returns:
        int -- number of sentences to return
    """
    if nominal <= 0:
        raise ValueError('Invalid summary length: ' + str(nominal))

    if nominal < 1:
        return int(nominal * total)

    return max([1, int(nominal)])
