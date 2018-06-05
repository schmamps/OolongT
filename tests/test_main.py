"""Test for OoolongT exports"""
from math import floor
from pathlib import Path
from random import randint

from oolongt.main import (
    score_sentences, summarize, get_slice_length,
    DEFAULT_SORT_KEY, DEFAULT_REVERSE, DEFAULT_LENGTH)
from oolongt.nodash import sort_by, pluck

from .constants import DATA_PATH, SAMPLES
from .helpers import (
    assert_ex, compare_float, get_samples, snip)
from .sample import Sample


def test_score_sentences():
    for samp in get_samples(*SAMPLES):
        title = samp.d['title']
        text = samp.d['text']

        for i, sentence in enumerate(score_sentences(title, text)):
            expected = samp.d['sentences'][i]['total_score']
            result = sentence['total_score']
            hint = snip(sentence['text'])

            assert compare_float(result, expected), assert_ex(
                'sentence score', result, expected, hint=hint)


def _get_expected_summaries(samp, length, sort_key, reverse):
    """Get text of top ranked sentences

    Arguments:
        samp {Sample} -- sample
        length {int} -- number of sentences to return
        sort_key {any} -- sort order of sentence Dicts
        reverse {bool} -- False: ASC, True: DESC (default: {False})

    Returns:
        List[str] -- text of sentences in specified order
    """
    length = length or DEFAULT_LENGTH
    sort_key = sort_key or DEFAULT_SORT_KEY
    reverse = reverse or DEFAULT_REVERSE

    ranked = sort_by(samp.d['sentences'], 'rank')
    sliced = ranked[:length]
    ordered = sort_by(sliced, sort_key, reverse=reverse)

    return pluck(ordered, 'text')


def _get_result_summaries(title, text, length, sort_key, reverse):
    """Summarize with correct keyword arguments

    Arguments:
        title {str} -- title of text
        text {str} -- body of content
        length {int} -- number of sentences to return
        sort_key {any} -- sort order of sentence Dicts
        reverse {bool} -- False: ASC, True: DESC (default: {False})

    Returns:
        List[str] -- text of sentences in specified order
    """
    opts = [
        (length, 'length'),
        (sort_key, 'sort_key'),
        (reverse, 'reverse')]

    kwargs = {}
    for opt in [opt for opt in opts if opt[0] is not None]:
        val, key = opt
        kwargs[key] = val

    return summarize(title, text, **kwargs)


def _test_summarize(sample_name, length, sort_key, reverse):
    """Test specified sample

    Arguments:
        sample_name {str} -- name of data source
        length {int} -- number of sentences to return
        sort_key {any} -- sort order of sentence Dicts
        reverse {bool} -- False: ASC, True: DESC (default: {False})
    """
    samp = Sample(DATA_PATH, sample_name)
    title = samp.d['title']
    text = samp.d['text']

    expecteds = _get_expected_summaries(
        samp, length, sort_key, reverse)
    results = _get_result_summaries(title, text, length, sort_key, reverse)

    assert (len(results) == len(expecteds)), assert_ex(
        'summary sentence count', len(results), length)

    for i, result in enumerate(results):
        expected = expecteds[i]
        hint = [snip(result), i]

        assert (result == expected), assert_ex(
            'summary [text at index]', result, expected, hint=hint)


def test_summarize():
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
                length = (idx_samp * idx_rev * idx_order) % len(SAMPLES)
                length += 1

                _test_summarize(sample_name, length, sort_key, reverse)


def test_get_slice_length():
    samples = [
        (0, 0, ValueError),
        (20, 1000, 20),
        (.1, 1000, 100)]

    for sample in samples:
        nominal, total, expected = sample
        test = False

        try:
            result = get_slice_length(nominal, total)
            test = (expected == result)

        except Exception as e:
            test = isinstance(e, expected)

        assert test, assert_ex(
            'slice length',
            result,
            expected,
            hint='nominal: ' + str(nominal))
