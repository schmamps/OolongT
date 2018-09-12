"""Test `ScoredSentence`"""
import typing

import kinda
from pytest import mark

from src.oolongt.summarizer.scored_sentence import (
    ScoredSentence, calc_decile, score_keyword_frequency, score_position,
    score_total)
from tests.helpers import check_exception, pad_to_longest
from tests.params.summarizer import (
    SPAM, SPAM_PARAMS, SPAM_RESULT, get_inst_comp, param_comp, param_decile,
    param_sentences)
from tests.typedefs import Sample, SampleSentence


@param_decile()
def test_calc_decile(
        index: int,
        total: int,
        expected: typing.Union[int, Exception]):
    """Test `calc_decile` in summarizer subpackage

    Arguments:
        index {int} -- index of sentence position (0-based)
        total {int} -- total number of sentences
        expected {typing.Union[int, Exception]} --
            decile of position (0-9) or error
    """
    try:
        received = calc_decile(index, total)

    except Exception as err:  # pylint: disable=broad-except
        received = check_exception(err, expected)

    assert received == expected


@mark.parametrize(
    'index,expected',
    [
        (0, .17),
        (99, .17),
        (100, .23),
        (999, .15),
        (-1, IndexError),
        (1000, IndexError)],
    ids=pad_to_longest([
        '0-of-1000',
        '99-of-1000',
        '100-of-1000',
        '999-of-1000',
        'neg-of-1000',
        '1000-of-1000']))
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
    expected = sentence.keyword_score
    received = score_keyword_frequency(sentence.dbs_score, sentence.sbs_score)

    assert kinda.eq(received, expected)


@param_sentences()
def test_score_total(sample: Sample, sentence: SampleSentence):
    """Test `score_total` in summarizer subpackage

    Arguments:
        sample {Sample} -- sample content
        sentence {SampleSentence} -- sentence from sample
    """
    expected = sentence.total_score
    received = score_total(
        sentence.title_score, sentence.keyword_score,
        sentence.length_score, sentence.position_score)

    assert kinda.eq(received, expected)
# pylint: enable=unused-argument


# pylint: disable=no-self-use
class TestScoredSentence:
    """Test `ScoredSentence`"""
    @mark.parametrize(
        'init,expected',
        [(
            SPAM_PARAMS,
            SPAM_RESULT[:-3] + list(float(x) for x in range(8, 11))), ],
        ids=pad_to_longest([SPAM, ]))
    def test__init_(self, init: list, expected: list):
        """Test `ScoredSentence` initialization

        Arguments:
            init {list} -- initialization parameters
            expected {list} -- expected property values
        """
        inst = ScoredSentence('', *range(6))
        inst._init_(*init)  # pylint: disable=protected-access
        received = get_inst_comp(inst)

        assert received == expected

    @mark.parametrize(
        'init,expected',
        [(SPAM_PARAMS, SPAM_RESULT)],
        ids=pad_to_longest([SPAM, ]))
    def test___init__(self, init: list, expected: list):
        """Test `ScoredSentence` initialization

        Arguments:
            init {list} -- initialization parameters
            expected {list} -- expected property values
        """
        inst = ScoredSentence(*init[:-3])
        received = get_inst_comp(inst)

        assert received == expected

    @mark.parametrize(
        'init,expected',
        [(SPAM_PARAMS, SPAM)],
        ids=pad_to_longest([SPAM]))
    def test___str__(self, init: list, expected: str):
        """Test `ScoredSentence` string cast

        Arguments:
            init {list} -- initialization parameters
            expected {str} -- expected value
        """
        inst = ScoredSentence(*init[:-3])
        received = str(inst)

        assert received == expected

    @mark.parametrize(
        'init,expected',
        [(
            SPAM_PARAMS,
            'ScoredSentence(\'spam\', 1, 3, 4.0, 5.0, 6.0, 7.0)')],
        ids=pad_to_longest([SPAM]))
    def test___repr__(self, init: list, expected: str):
        """Test `ScoredSentence` REPR

        Arguments:
            init {list} -- initialization parameters
            expected {str} -- expected value
        """
        inst = ScoredSentence(*init[:-3])
        received = repr(inst)

        assert received == expected

    # pylint: disable=unused-argument
    @param_comp()
    def test___eq__(
            self,
            sent_a: ScoredSentence,
            sent_b: ScoredSentence,
            is_lt: bool,
            is_eq: bool):
        """Test `ScoredSentence` equality

        Arguments:
            sent_a {ScoredSentence} -- sentence A
            sent_b {ScoredSentence} -- sentence B
            is_lt {bool} -- sentence A is Less Than sentence B
            is_eq {bool} -- sentence A is EQual to sentence B
        """
        expected = is_eq
        received = sent_a == sent_b

        assert received == expected

    @param_comp()
    def test___lt__(
            self,
            sent_a: ScoredSentence,
            sent_b: ScoredSentence,
            is_lt: bool,
            is_eq: bool):
        """Test `ScoredSentence` less-than

        Arguments:
            sent_a {ScoredSentence} -- sentence A
            sent_b {ScoredSentence} -- sentence B
            is_lt {bool} -- sentence A is Less Than sentence B
            is_eq {bool} -- sentence A is EQual to sentence B
        """
        expected = is_lt
        received = sent_a < sent_b

        assert received == expected

    @param_comp()
    def test___gt__(
            self,
            sent_a: ScoredSentence,
            sent_b: ScoredSentence,
            is_lt: bool,
            is_eq: bool):
        """Test `ScoredSentence` greater-than

        Arguments:
            sent_a {ScoredSentence} -- sentence A
            sent_b {ScoredSentence} -- sentence B
            is_lt {bool} -- sentence A is Less Than sentence B
            is_eq {bool} -- sentence A is EQual to sentence B
        """
        expected = (not is_lt) and (not is_eq)
        received = sent_a > sent_b

        assert received == expected
