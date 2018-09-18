"""Test ScoredKeyword"""
import typing

from src.oolongt.constants import KEYWORD_SCORE_K
from src.oolongt.parser.scored_keyword import (
    ScoredKeyword, compare_keywords, compare_score, compare_word,
    score_keyword)
from tests.helpers import check_exception
from tests.params.parser import (
    param_compare_keywords, param_compare_score, param_compare_word,
    param_score_keyword, parametrize_words)


@param_score_keyword()
def test_score_keyword(
        count: int,
        total: int,
        expected: typing.Union[float, Exception]):
    """Test score_keyword in parser subpackage

    Arguments:
        count {int} -- instances of word in text
        total {int} -- total number of words in text
        expected {typing.Union[float, Exception]} -- expected outcome
    """
    try:
        received = score_keyword(count, total)

    except Exception as err:  # pylint: disable=broad-except
        received = check_exception(err, expected)

    assert received == expected


@param_compare_score()
def test_compare_score(score_a: float, score_b: float, expected: int):
    """Test compare_score in parser subpackage

    Arguments:
        score_a {float} -- score A
        score_b {float} -- score B
        expected {int} -- comparison of values
    """
    received = compare_score(score_a, score_b)

    assert received == expected


@param_compare_word()
def test_compare_word(word_a: str, word_b: str, expected: int):
    """Test compare_word in parser subpackage

    Arguments:
        word_a {str} -- word A
        word_b {str} -- word B
        expected {int} -- comparison of values
    """
    received = compare_word(word_a, word_b)

    assert received == expected


@param_compare_keywords()
def test_compare_keywords(
        kw_a: ScoredKeyword,
        kw_b: ScoredKeyword,
        is_lt: bool,
        is_eq: bool,
        reason: str):
    """Test compare_keywords in parser subpackage

    Arguments:
        kw_a {ScoredKeyword} -- keyword A
        kw_b {ScoredKeyword} -- keyword B
        is_lt {bool} -- keyword A is Less Than keyword B
        is_eq {bool} -- keyword A is EQual to keyword B
    """
    equality = (0, 0, 0)
    received = compare_keywords(kw_a, kw_b)
    assert_msg = 'reason: {}'.format(
        {'s': 'score', 'l': 'length', 'w': 'word'}[reason])

    if is_lt:
        assert received < equality, assert_msg

    elif is_eq:
        assert received == equality, assert_msg

    else:
        assert received > equality, assert_msg


# pylint: disable=no-self-use,invalid-name
class TestScoredKeyword:
    """Test `ScoredKeyword`"""
    @parametrize_words()
    def test___init__(self, word: str, count: int, total: int):
        """Test `ScoredKeyword` initialization

        Arguments:
            word {str} -- word property of ScoredKeyword
            count {int} -- count property of ScoredKeyword
            total {int} -- of property of ScoredKeyword
        """
        expected = (word, count, total, KEYWORD_SCORE_K)

        inst = ScoredKeyword(word, count, total)
        received = (inst.word, inst.count, inst.of, inst.score)

        assert received == expected

    @parametrize_words()
    def test___str__(self, word: str, count: int, total: int):
        """Test `ScoredKeyword` string cast

        Arguments:
            word {str} -- word property of ScoredKeyword
            count {int} -- count property of ScoredKeyword
            total {int} -- of property of ScoredKeyword
        """
        expected = word

        inst = ScoredKeyword(word, count, total)
        received = inst.word

        assert received == expected

    @parametrize_words()
    def test___repr__(self, word: str, count: int, total: int):
        """Test `ScoredKeyword` REPR

        Arguments:
            word {str} -- word property of ScoredKeyword
            count {int} -- count property of ScoredKeyword
            total {int} -- of property of ScoredKeyword
        """
        expected = 'ScoredKeyword({!r}, {}, {})'.format(word, count, total)

        inst = ScoredKeyword(word, count, total)
        received = repr(inst)

        assert received == expected
