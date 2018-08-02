""" Helpers for testing """
from random import shuffle

from tests.typing.sample import Sample
from tests.typing.sample_keyword import SampleKeyword

from tests.constants import DATA_PATH


def snip(val, max_len=20, list_separator=', ', ellip="..."):
    # type: (any, int, str, str) -> str
    """Truncate `val` to specified length

    Arguments:
        val {str} -- string to snip

    Keyword Arguments:
        max_len {int} -- maximum length of string (default: {20})
        list_separator {str} -- if list passed,
            string to join members (default: {' '})
        ellip {str} -- filler text if truncated (default: {"..."})

    Returns:
        str -- text, truncated if necessary

    >>> snip('1234567890')
    '1234567890'
    >>> snip('123456789012345678901')
    '12345678901234567...'
    >>> snip('1234567890', max_len=9 ellip='!')
    '12345678!'
    """
    text = list_separator.join(val) if isinstance(val, list) else str(val)

    if len(text) <= max_len:
        return text

    clip = text[:max_len - len(ellip)]

    return clip + ellip


def randomize_list(src):
    # type: (list[any]) -> list[any]
    """Get a reordered copy of `src`

    Arguments:
        src {list} -- source list

    Returns:
        list -- copy of source list in different order (if possible)

    >>> [] == randomize_list([])
    True
    >>> [1, 2, 3] == randomize_list([1, 2, 3])
    False
    """
    dupe = list(src)
    while (dupe == src and len(src) > 1):
        shuffle(dupe)

    return dupe


def assert_ex(msg, received, expected, hint=None):
    # type: (str, any, any, any) -> str
    """Generate detailed AssertionError messages

    Arguments:
        msg {str} -- description of test
        received {any} -- received value
        expected {any} -- expected value

    Keyword Arguments:
        hint {any} -- add'l detail for description (default: {None})

    Returns:
        str -- detailed error message
    """
    if hint is not None:
        hint = ' (' + repr(hint) + ')'
    else:
        hint = ''

    res_str = str(received)
    exp_str = str(expected)

    return '\n'.join([
        msg + hint,
        'received > ' + res_str,
        'expected > ' + exp_str])


def get_sample(sample_name):
    # type: (str) -> Sample
    """Get Sample by name

    Arguments:
        sample_name {str} -- name of sample

    Returns:
        Sample -- sample data
    """
    return Sample(DATA_PATH, sample_name)


def get_samples(sample_names):
    # type (list[str]) -> Iterable[Sample]
    """Get Samples by name

    Returns:
        Iterator[Sample] - iterable of samples
    """
    for sample_name in sample_names:
        yield get_sample(sample_name)


def get_sample_ids(sample_names):
    # TODO: more detail?
    return pad_to_longest(sample_names)


def get_sample_sentences(sample_names):
    # type (list[str]) -> Iterable[tuple[Sample, SampleSentence]]
    """Get Sample, each sentence from Sample

    Arguments:
        sample_names {list[str]} -- names of samples

    Returns:
        Iterator[Sample] -- Iterator of Samples
    """
    for sample_name in sample_names:
        samp = get_sample(sample_name)

        for sentence in samp.sentences:
            yield samp, sentence


def get_sample_sentence_ids(sample_names):
    ids = []
    for sample_name in sample_names:
        samp = get_sample(sample_name)

        for sentence in samp.sentences:
            ids.append('{0}: {1}'.format(samp.name, sentence.id))

    return ids


def check_exception(catch, expected):
    # type: (Exception, any) -> any
    """Compare caught exception to expected value

    Arguments:
        catch {Exception} -- caught exception
        expected {any} -- expected exception (or value if unexpected)

    Returns:
        any -- expected if match, catch if no match
    >>> check_exception(ValueError, ValueError)
    ValueError
    >>> check_exception(KeyError, IndexError)
    KeyError
    >>> check_exception(IndexError, 0)
    IndexError
    """
    try:
        if isinstance(catch, expected):
            return expected

    except TypeError:
        pass

    return catch


def pad_to_longest(strs):
    pad_len = max([len(x) for x in strs])
    pad_str = ' ' * pad_len
    padded = [(x + pad_str)[:pad_len] for x in strs]

    return padded
