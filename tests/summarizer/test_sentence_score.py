"""Test `SentenceScore`"""
import kinda
import typing
from tests.helpers import check_exception

from src.oolongt.summarizer.sentence_score import (
    calc_rank, score_keyword_frequency, score_position,
    score_total)
from tests.params.summarizer import (
    param_calc_rank, param_score_position, param_sentences)
from tests.typings import Sample, SampleSentence


@param_calc_rank()
def test_calc_rank(
        index: int,
        total: int,
        num_ranks: int,
        expected: typing.Union[int, Exception]):
    """Test `calc_rank` in summarizer subpackage

    Arguments:
        index {int} -- index of sentence position (0-based)
        total {int} -- total number of sentences
        expected {typing.Union[int, Exception]} --
            decile of position (0-9) or error
    """
    try:
        received = calc_rank(index, total, num_ranks)

    except Exception as err:  # pylint: disable=broad-except
        received = check_exception(err, expected)

    assert received == expected


@param_score_position()
def test_score_position(index: int, expected: typing.Union[float, Exception]):
    """Test `score_position` in summarizer subpackage

    Arguments:
        index {int} -- index of sentence position (0-based)
        expected {typing.Union[float, Exception]} -- position score or error
    """
    total = 1000

    try:
        received = score_position(index, total)
        test = kinda.eq(received, expected)

    except Exception as err:  # pylint: disable=broad-except
        received = check_exception(err, expected)
        test = (received == expected)

    assert test


# pylint: disable=unused-argument
@param_sentences()
def test_score_keyword_frequency(sample: Sample, sentence: SampleSentence):
    """Test `score_keyword_frequency` in summarizer subpackage

    Arguments:
        sample {Sample} -- sample content
        sentence {SampleSentence} -- sentence from sample
    """
    expected = sentence.score.keyword
    received = score_keyword_frequency(sentence.score.dbs, sentence.score.sbs)

    assert kinda.eq(received, expected)


@param_sentences()
def test_score_total(sample: Sample, sentence: SampleSentence):
    """Test `score_total` in summarizer subpackage

    Arguments:
        sample {Sample} -- sample content
        sentence {SampleSentence} -- sentence from sample
    """
    expected = sentence.score.total
    received = score_total(
        sentence.score.title, sentence.score.keyword,
        sentence.score.length, sentence.score.position)

    assert kinda.eq(received, expected)
# pylint: enable=unused-argument
