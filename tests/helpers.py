""" Helpers for testing """
import typing
from random import shuffle

from src.oolongt.typings import AnyList, StringList
from tests.constants import TEXT_PATH
from tests.typings.sample import Sample


def snip(
        val: typing.Any,
        max_len: int = 20,
        list_separator: str = ', ',
        ellip: str = '...'):
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


def randomize_list(src: AnyList) -> AnyList:
    """Get a reordered copy of `src`

    Arguments:
        src {AnyList} -- source list

    Returns:
        AnyList --
            copy of source list in different order (if possible)

    >>> [] == randomize_list([])
    True
    >>> [1, 2, 3] == randomize_list([1, 2, 3])
    False
    """
    dupe = list(src)
    while (dupe == src and len(src) > 1):
        shuffle(dupe)

    return dupe


def assert_ex(
        msg: str,
        received: typing.Any,
        expected: typing.Any,
        hint: typing.Any = None):
    """Generate detailed assertion messages

    Arguments:
        msg {str} -- description of test
        received {typing.Any} -- received value
        expected {typing.Any} -- expected value

    Keyword Arguments:
        hint {typing.Any} -- add'l detail for description (default: {None})

    Returns:
        str -- detailed error message
    """
    hint_str = '' if hint is None else '({!r})'.format(hint)

    return '{} {}\nreceived > {}\nexpected > {}'.format(
        msg, hint_str, received, expected)


def get_sample(sample_name: str) -> Sample:
    """Get Sample by name

    Arguments:
        sample_name {str} -- name of sample

    Returns:
        Sample -- sample data
    """
    return Sample(TEXT_PATH, sample_name)


def check_exception(catch: Exception, expected: typing.Any) -> typing.Any:
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


def pad_to_longest(vals: AnyList) -> StringList:
    """Pad all strings to length of longest in list

    Arguments:
        strs {StringList} -- string list

    Returns:
        StringList -- list of strings
    """
    strs = [str(x) for x in vals]
    pad_len = max([len(x) for x in strs])
    pad_str = ' ' * pad_len
    padded = [(x + pad_str)[:pad_len] for x in strs]

    return padded


def index_of(index: int, of: int):  # pylint: disable=invalid-name
    """Return '$index of $of'

    Arguments:
        index {int} -- index
        of {int} -- count

    Returns:
        str -- string
    """
    return '{!r} of {!r}'.format(index, of)


# pylint: disable=unused-argument
def return_true(*args, **kwargs):
    """Always return True

    Returns:
        bool -- True
    """
    return True


def return_false(*args, **kwargs):
    """Always return False

    Returns:
        bool -- False
    """
    return False
