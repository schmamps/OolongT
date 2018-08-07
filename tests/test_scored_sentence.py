from pytest import mark

from oolongt import roughly
from oolongt.typing.scored_sentence import (ScoredSentence, calc_decile,
                                            score_keyword_frequency,
                                            score_position, score_total)

from .constants import SAMPLES
from .helpers import (assert_ex, check_exception, get_sample_ids,
                      get_sample_sentence_ids, get_sample_sentences,
                      get_samples, pad_to_longest)


@mark.parametrize(
    'index,of,expected',
    [
        (0, 10, 1),
        (9, 100, 1),
        (1, 10, 2),
        (2, 10, 3),
        (3, 10, 4),
        (4, 10, 5),
        (5, 10, 6),
        (6, 10, 7),
        (7, 10, 8),
        (8, 10, 9),
        (9, 10, 10),
        (-1, 100, ValueError),
        (10, 10, ValueError),
        (10, 0, ValueError),
    ],
    ids=[
        'index:  0, of:  10 (  1)',
        'index:  1, of:  10 (  2)',
        'index:  2, of:  10 (  3)',
        'index:  3, of:  10 (  4)',
        'index:  4, of:  10 (  5)',
        'index:  5, of:  10 (  6)',
        'index:  6, of:  10 (  7)',
        'index:  7, of:  10 (  8)',
        'index:  8, of:  10 (  9)',
        'index:  9, of:  10 ( 10)',
        'index:  9, of: 100 (  1)',
        'index: -1, of: 100 (err)',
        'index: 10, of:  10 (err)',
        'index: 10, of:   0 (err)',
    ])
def test_calc_decile(index, of, expected):
    try:
        received = calc_decile(index, of)

    except ValueError as e:
        received = check_exception(e, expected)

    assert (received == expected), assert_ex(
        'calculate decile',
        received,
        expected,
        hint='/'.join([str(index), str(of)]))


@mark.parametrize(
    'index,expected',
    [
        (0,   .17),
        (99,  .17),
        (100, .23),
        (999, .15),
        (-1,  ValueError),
        (1000, ValueError),
    ],
    ids=[
        'first decile, first sentence  (   0 of 1000)',
        'first decile, last sentence   (  99 of 1000)',
        'second decile, first sentence ( 100 of 1000)',
        'last decile, last sentence    ( 999 of 1000)',
        'index out of range: low       (  -1 of 1000)',
        'index out of range: high      (1000 of 1000)',
    ])
def test_score_position(index, expected):
    of = 1000

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


@mark.parametrize(
    'sample,sentence',
    get_sample_sentences(SAMPLES),
    ids=get_sample_sentence_ids(SAMPLES))
def test_score_keyword_frequency(sample, sentence):
    # type: (ScoredSentence) -> None
    expected = sentence.keyword_score
    received = score_keyword_frequency(sentence.dbs_score, sentence.sbs_score)

    assert roughly.eq(received, expected), assert_ex(
        'keyword frequency score',
        received,
        expected)


@mark.parametrize(
    'sample,sentence',
    get_sample_sentences(SAMPLES),
    ids=get_sample_sentence_ids(SAMPLES))
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
