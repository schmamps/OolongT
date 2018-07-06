import pytest

from oolongt.typing.scored_sentence import (ScoredSentence,
                                            score_keyword_frequency,
                                            score_position, score_total)

from .constants import SAMPLES
from .helpers import (assert_ex, check_exception, get_sample_sentences,
                      get_samples, roughly)


@pytest.mark.parametrize('index,of,expected', [
    (0, 10, .17),             # first decile
    (0, 5, .23),              # second decile
    (999, 1000, .15),         # last sentence
    (999,    0, ValueError),  # out of range
    (999,  999, ValueError),  # out of range
])
def test_score_position(index, of, expected):
    try:
        received = score_position(index, of)
        test = roughly.eq(received, expected)

    except ValueError as e:
        received = check_exception(e, expected)
        test = (received == expected)

    assert test, assert_ex(
        'sentence position score',
        received,
        expected,
        hint=' of '.join([str(index), str(of)]))


@pytest.mark.parametrize('sample,sentence', get_sample_sentences(SAMPLES))
def test_score_keyword_frequency(sample, sentence):
    # type: (ScoredSentence) -> None
    expected = sentence.keyword_score
    received = score_keyword_frequency(sentence.dbs_score, sentence.sbs_score)

    assert roughly.eq(received, expected), assert_ex(
        'keyword frequency score',
        received,
        expected)


@pytest.mark.parametrize('sample,sentence', get_sample_sentences(SAMPLES))
def test_score_total(sample, sentence):
    # type: (ScoredSentence) -> None
    expected = sentence.total_score
    received = score_total(
        sentence.title_score, sentence.keyword_score,
        sentence.length_score, sentence.position_score)

    assert roughly.eq(received, expected), assert_ex(
        'keyword frequency score',
        received,
        expected)


class TestScoredSentence:
    pass
