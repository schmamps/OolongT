""" Helpers for testing """
from random import shuffle

from pytest import approx

from .constants import DATA_PATH
from .sample import Sample


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


def compare_list(left, right):
    # type: (list, list) -> str
    """Compare `left` as a subset of `right`

    Arguments:
        left {list[Any]} - reference list
        right {list[Any]} - list to compare against

    Returns:
        str -- length of left list, REPR of exclusive values

    >>> compare_list([1, 2, 3], [2, 3, 4])
    'len: 3, exclusive: ['1']'
    >>> compare_list([1, 2, 3], [1, 2, 3, 4])
    'len: 3, exclusive: []'
    """
    len_str = 'len: ' + str(len(left))
    diff_str = 'exclusive: ' + str([repr(x) for x in left if x not in right])

    return ', '.join([len_str, diff_str])


def get_compare_value(val, rel=0.000001):
    if isinstance(val, float):
        return approx(val, rel=rel)

    return val


def compare_dict(left, right, keys=[], ignore=[]):
    # type: (dict, dict, list[any], list[any]) -> bool
    """Compare `left` as a subset of `right`

    Arguments:
        left {dict} -- lowest common denominator Dict
        right {dict} -- Dict that should contain the same key/value pairs

    Keyword Arguments:
        keys {list[any]} -- keys to compare (Default: left.keys())
        ignore {list[any]} - keys to ignore (Default: [])

    >>> compare_dict({1: 1}, {1: 1})
    True
    >>> compare_dict({1: 1, 2: 2}, {1: 1})
    False
    >>> compare_dict({1: 1, 2: 2}, {1: 1}, keys=[1])
    True
    """
    keys = [key for key in (keys or left.keys()) if key not in ignore]

    for key in keys:
        left_val = left[key]
        right_val = get_compare_value(right.get(key, None))

        if (left_val != right_val):
            break

    return (left_val == right_val)


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

    if isinstance(received, list) and isinstance(expected, list):
        res_str = compare_list(received, expected)
        exp_str = compare_list(expected, received)

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
    # type (list[str]) -> list[Sample]
    """Get Samples by name

    Returns:
        Iterator[Sample] - iterable of samples
    """
    for sample_name in sample_names:
        yield get_sample(sample_name)


def get_sample_sentences(sample_names):
    # type (list[str]) -> list[dict]
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
