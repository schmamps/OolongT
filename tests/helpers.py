""" Helpers for testing """
import typing
from random import shuffle

from tests.constants import DATA_PATH
from tests.typedefs.sample import Sample
from tests.typedefs.sample_keyword import SampleKeyword
from tests.typedefs.sample_sentence import SampleSentence


def snip(
        val: typing.Any,
        max_len: int = 20,
        list_separator: str = ', ',
        ellip: str = "..."):
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


def randomize_list(
        src: typing.List[typing.Any]
        ) -> typing.List[typing.Any]:
    """Get a reordered copy of `src`

    Arguments:
        src {typing.List[typing.Any]} -- source list

    Returns:
        typing.List[typing.Any] --
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
    return Sample(DATA_PATH, sample_name)


def get_samples(sample_names: typing.List[str]) -> typing.Iterable[Sample]:
    """Get Samples by name

    Returns:
        typing.Iterable[Sample] - iterable of samples
    """
    for sample_name in sample_names:
        yield get_sample(sample_name)


def get_sample_ids(sample_names: typing.List[str]) -> typing.List[str]:
    return pad_to_longest(['src: {}'.format(x) for x in sample_names])


def get_sample_sentences(
        sample_names: typing.List[str],
        ) -> typing.Iterable[typing.Tuple[Sample, SampleSentence]]:
    """Get Sample, each sentence from Sample

    Arguments:
        sample_names {typing.List[str]} -- names of samples

    Returns:
        typing.Iterable[Sample] -- Iterator of Samples
    """
    for sample_name in sample_names:
        samp = get_sample(sample_name)

        for sentence in samp.sentences:
            yield samp, sentence


def get_sample_sentence_ids(
        sample_names: typing.List[str]
        ) -> typing.List[str]:
    """List friendly names of sample sentences

    Returns:
        typing.List[str] -- IDs of sample sentences
    """
    ids = []
    for sample_name in sample_names:
        samp = get_sample(sample_name)

        for sentence in samp.sentences:
            ids.append('src: {}, sent: {}'.format(samp.name, sentence.id))

    return pad_to_longest(ids)


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


def pad_to_longest(vals: typing.List[typing.Any]) -> typing.List[str]:
    """Pad all strings to length of longest in list

    Arguments:
        strs {typing.List[str]} -- string list

    Returns:
        typing.List[str] -- list of strings
    """
    strs = [str(x) for x in vals]
    pad_len = max([len(x) for x in strs])
    pad_str = ' ' * pad_len
    padded = [(x + pad_str)[:pad_len] for x in strs]

    return padded


def index_of(index, of):
    return '{!r} of {!r}'.format(index, of)
