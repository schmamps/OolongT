"""Test text subpackage"""
import typing

import kinda

from src.oolongt import score_body_sentences, summarize
from src.oolongt.text.text import get_slice_length
from src.oolongt.typings import StringList
from tests.constants import SAMPLES, TEXT_PATH
from tests.helpers import assert_ex, check_exception, snip
from tests.params.summarizer import param_samples
from tests.params.text import param_get_slice_length, param_summarize
from tests.typings.sample import Sample
from tests.typings.sample_sentence import SampleSentence

SampleSentenceList = typing.List[SampleSentence]


@param_samples()
def test_score_body_sentences(samp: Sample) -> None:
    """Test `score_body_sentences` for text subpackage

    Arguments:
        samp {Sample} -- sample data
    """
    for i, sent in enumerate(score_body_sentences(samp.body, samp.title)):
        expected = samp.sentences[i].score.total
        received = sent.score.total

        assert kinda.eq(received, expected), assert_ex(
            'sentence score',
            received,
            expected,
            hint=snip(sent.text))


def _get_best_sentences(
        samp: Sample,
        limit: int) -> SampleSentenceList:
    """List top rated sentences in content order

    Arguments:
        samp {Sample} -- sample data
        limit {int} -- number of sentences to return

    Returns:
        SampleSentenceList -- list of sentences
    """
    ranked = sorted(samp.sentences, reverse=True)

    return sorted(ranked[:limit], key=lambda sent: sent.index)


def _get_expected_sentences(samp: Sample, limit: int) -> StringList:
    """Get text of top ranked sentences

    Arguments:
        samp {Sample} -- sample
        limit {int} -- number of sentences to return

    Returns:
        StringList -- list of sentence strings
    """
    best_sentences = _get_best_sentences(samp, limit)

    return [sent.text for sent in best_sentences]


def _get_received_sentences(title: str, text: str, limit: int) -> StringList:
    """Summarize with correct keyword arguments

    Arguments:
        title {str} -- title of text
        text {str} -- body of content
        limit {int} -- number of sentences to return

    Returns:
        StringList -- list of sentence strings
    """
    scored_sentences = summarize(text, title, limit=limit)

    return scored_sentences


def permute_test_summarize() -> typing.Iterable[typing.Tuple[str, int]]:
    """Parametrize for `test_summarize` """
    for sample_name in SAMPLES:
        for limit in range(1, 8, 2):
            yield (sample_name, limit)


@param_summarize()
def test_summarize(sample_name: str, limit: int) -> None:
    """Test `summarize` in text subpackage

    Arguments:
        sample_name {str} -- name of data source
        limit {int} -- number of sentences to return
    """
    samp = Sample(TEXT_PATH, sample_name)
    title = samp.title
    text = samp.body

    expecteds = _get_expected_sentences(samp, limit)
    receiveds = _get_received_sentences(title, text, limit)

    assert (len(receiveds) == len(expecteds)), assert_ex(
        'summary sentence count', len(receiveds), limit)

    for i, received in enumerate(receiveds):
        expected = expecteds[i]

        assert (received == expected), assert_ex(
            'summary [text at index]',
            received,
            expected,
            hint=[snip(received), i])


@param_get_slice_length()
def test_get_slice_length(
        nominal: typing.Any,
        total: int,
        expected: typing.Any) -> None:
    """Test `get_slice_length` in text subpackage

    Arguments:
        nominal {float} -- exact number (int) or percentage (0 < nominal < 1)
        total {int} -- number of items to slice from
        expected {typing.Any} -- expected Exception/number of items
    """
    try:
        received = get_slice_length(nominal, total)

    except ValueError as err:
        received = check_exception(err, expected)

    assert (expected == received), assert_ex(
        'slice length',
        received,
        expected,
        hint='nominal: {!r}'.format(nominal))
