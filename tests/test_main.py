"""Test for OoolongT exports"""
from math import floor
from pathlib import Path
from random import randint

from pytest import mark

from oolongt import roughly
from oolongt.main import (DEFAULT_LENGTH, get_slice_length,
                          score_body_sentences, summarize)
from tests.constants import DATA_PATH, SAMPLES
from tests.helpers import (assert_ex, check_exception, get_sample_ids,
                           get_samples, pad_to_longest, snip)
from tests.typing.sample import Sample
from tests.typing.sample_sentence import SampleSentence


@mark.parametrize(
    'samp',
    get_samples(SAMPLES),
    ids=pad_to_longest(get_sample_ids(SAMPLES)))
def test_score_body_sentences(samp):
    """Test main.score_sentences()

    Arguments:
        samp {Sample} -- sample data
    """
    for i, sentence in enumerate(score_body_sentences(samp.body, samp.title)):
        expected = samp.sentences[i].total_score
        received = sentence.total_score

        assert roughly.eq(received, expected), assert_ex(
            'sentence score',
            received,
            expected,
            hint=snip(sentence.text))


def _get_best_sentences(samp, length):
    ranked = sorted(samp.sentences, reverse=True)

    return sorted(ranked[:length], key=lambda sent: sent.index)


def _get_expected_sentences(samp, length):
    # type: (Sample, int) -> list[str]
    """Get text of top ranked sentences

    Arguments:
        samp {Sample} -- sample
        length {int} -- number of sentences to return

    Returns:
        list[str] -- text of sentences in specified order
    """
    best_sentences = _get_best_sentences(samp, length)

    return [sent.text for sent in best_sentences]


def _get_received_sentences(title, text, length):
    # type: (str, str, int) -> list[str]
    """Summarize with correct keyword arguments

    Arguments:
        title {str} -- title of text
        text {str} -- body of content
        length {int} -- number of sentences to return

    Returns:
        list[str] -- text of sentences in specified order
    """
    scored_sentences = summarize(title, text, length=length)

    return scored_sentences


def permute_test_summarize():
    # type () -> Iterable[tuple[str, int]]
    """Generate parameters for test_summarize() """
    for sample_name in SAMPLES:
        for length in range(1, 8, 2):
            yield (sample_name, length)


@mark.parametrize('sample_name,length', permute_test_summarize())
def test_summarize(sample_name, length):
    """Test specified sample

    Arguments:
        sample_name {str} -- name of data source
        length {int} -- number of sentences to return
    """
    samp = Sample(DATA_PATH, sample_name)
    title = samp.title
    text = samp.body

    expecteds = _get_expected_sentences(samp, length)
    receiveds = _get_received_sentences(title, text, length)

    assert (len(receiveds) == len(expecteds)), assert_ex(
        'summary sentence count', len(receiveds), length)

    for i, received in enumerate(receiveds):
        expected = expecteds[i]

        assert (received == expected), assert_ex(
            'summary [text at index]',
            received,
            expected,
            hint=[snip(received), i])


@mark.parametrize(
    'nominal,total,expected',
    [
        (20, 1000, 20),
        (1001, 1000, 1000),
        (.1, 1000, 100),
        (0, 0, ValueError),
    ],
    ids=pad_to_longest([
        'nominal: >= 1, total: > nominal == nominal',
        'nominal: >= 1, total: < nominal == total',
        'nominal: < 1,  total: > 1       == fraction of total',
        'cannot be sliced',
    ]))
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
