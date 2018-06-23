"""Test for OoolongT exports"""
from math import floor
from pathlib import Path
from pytest import approx, mark
from random import randint

from oolongt.main import (
    score_sentences, summarize, get_slice_length,
    DEFAULT_SORT_KEY, DEFAULT_REVERSE, DEFAULT_LENGTH)
from oolongt.nodash import sort_by, pluck

from .constants import DATA_PATH, SAMPLES
from .helpers import (
    assert_ex, get_samples, snip, check_exception)
from .sample import Sample


@mark.parametrize('samp', get_samples(SAMPLES))
def test_score_sentences(samp):
    """Test main.score_sentences()

    Arguments:
        samp {Sample} -- sample data
    """
    title = samp.title
    text = samp.text

    for i, sentence in enumerate(score_sentences(title, text)):
        expected = samp.d['sentences'][i]['total_score']
        received = sentence['total_score']
        hint = snip(sentence['text'])

        assert approx(received, expected), assert_ex(
            'sentence score', received, expected, hint=hint)


def _get_expected_summaries(samp, length, sort_key, reverse):
    # type: (Sample, int, any, bool) -> list[str]
    """Get text of top ranked sentences

    Arguments:
        samp {Sample} -- sample
        length {int} -- number of sentences to return
        sort_key {any} -- sort order of sentence Dicts
        reverse {bool} -- False: ASC, True: DESC (default: {False})

    Returns:
        list[str] -- text of sentences in specified order
    """
    length = length or DEFAULT_LENGTH
    sort_key = sort_key or DEFAULT_SORT_KEY
    reverse = reverse or DEFAULT_REVERSE

    ranked = sort_by(samp.d['sentences'], 'rank')
    sliced = ranked[:length]
    ordered = sort_by(sliced, sort_key, reverse=reverse)

    return pluck(ordered, 'text')


def _get_received_summaries(title, text, length, sort_key, reverse):
    # type: (str, str, int, any, bool) -> list[str]
    """Summarize with correct keyword arguments

    Arguments:
        title {str} -- title of text
        text {str} -- body of content
        length {int} -- number of sentences to return
        sort_key {any} -- sort order of sentence Dicts
        reverse {bool} -- False: ASC, True: DESC (default: {False})

    Returns:
        list[str] -- text of sentences in specified order
    """
    opts = [
        (length, 'length'),
        (sort_key, 'sort_key'),
        (reverse, 'reverse')]

    kwargs = {}
    for opt in [opt for opt in opts if opt[0] is not None]:
        val, key = opt
        kwargs[key] = val

    summaries = summarize(title, text, **kwargs)

    return summaries


def permute_test_summarize():
    # type () -> list[tuple[str, int, any, bool]]
    """Generate parameters for test_summarize()
    """
    sort_keys = [
        None,
        'order',
        'total_score',
        'title_score',
        'length_score',
        'position_score',
        'keyword_score',
        'text']
    reverse_keys = [None, True, False]

    for idx_samp, sample_name in enumerate(SAMPLES):
        for idx_rev, reverse in enumerate(reverse_keys):
            for idx_order, sort_key in enumerate(sort_keys):
                length = (idx_samp * idx_rev * idx_order) % 8
                yield (sample_name, length + 1, sort_key, reverse)


@mark.parametrize(
    'sample_name,length,sort_key,reverse', permute_test_summarize())
def test_summarize(sample_name, length, sort_key, reverse):
    """Test specified sample

    Arguments:
        sample_name {str} -- name of data source
        length {int} -- number of sentences to return
        sort_key {any} -- sort order of sentence Dicts
        reverse {bool} -- False: ASC, True: DESC (default: {False})
    """
    samp = Sample(DATA_PATH, sample_name)
    title = samp.title
    text = samp.text

    expecteds = _get_expected_summaries(
        samp, length, sort_key, reverse)
    receiveds = _get_received_summaries(title, text, length, sort_key, reverse)

    assert (len(receiveds) == len(expecteds)), assert_ex(
        'summary sentence count', len(receiveds), length)

    for i, received in enumerate(receiveds):
        expected = expecteds[i]
        hint = [snip(received), i]

        assert (received == expected), assert_ex(
            'summary [text at index]', received, expected, hint=hint)


@mark.parametrize('nominal,total,expected', [
    (0, 0, ValueError),
    (20, 1000, 20),
    (.1, 1000, 100),
])
def test_get_slice_length(nominal, total, expected):
    """Test main.get_slice_length()

    Arguments:
        nominal {float} -- exact number (int) or percentage (float: 0-1)
        total {int} -- number of items to slice from
        expected {int} -- expected number of items to slice
    """
    received = None

    try:
        received = get_slice_length(nominal, total)

    except ValueError as e:
        received = check_exception(e, expected)

    assert (expected == received), assert_ex(
        'slice length',
        received,
        expected,
        hint='nominal: ' + str(nominal))
