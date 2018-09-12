"""Test ScoredKeyword"""
import typing

from pytest import mark

from src.oolongt.constants import KEYWORD_SCORE_K
from src.oolongt.parser.scored_keyword import (
    ScoredKeyword, compare_keywords, compare_score, compare_word,
    score_keyword)
from tests.helpers import check_exception, pad_to_longest
from tests.params.parser import gen_scored_keyword as gen_inst
from tests.params.parser import parametrize_words


@mark.parametrize(
    'count,total,expected',
    [
        (1, 1, KEYWORD_SCORE_K),
        (-1, 1, ValueError),
        (1, 0, ValueError),
        (2, 1, ValueError), ],
    ids=pad_to_longest(['normal', 'sub0', 'div0/neg', 'overmax', ]))
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


@mark.parametrize(
    'score_a,score_b,expected',
    [
        (0.0, 1.0, -1),
        (0.999999999999999999, 1.0, 0),
        (1.000000000000000000, 1.0, 0),
        (1.000000000000000001, 1.0, 0),
        (2, 1.0, 1), ],
    ids=pad_to_longest([
        'quite_lt',
        'lt_but_eq',
        'exact_eq',
        'gt_but_eq',
        'quite_gt', ]))
def test_compare_score(score_a: float, score_b: float, expected: int):
    """Test compare_score in parser subpackage

    Arguments:
        score_a {float} -- score A
        score_b {float} -- score B
        expected {int} -- comparison of values
    """
    received = compare_score(score_a, score_b)

    assert received == expected


@mark.parametrize(
    'word_a,word_b,expected',
    [('spal', 'spam', -1), ('spam', 'spam', 0), ('span', 'spam', 1)],
    ids=pad_to_longest(['lt', 'eq', 'gt'])
)
def test_compare_word(word_a: str, word_b: str, expected: int):
    """Test compare_word in parser subpackage

    Arguments:
        word_a {str} -- word A
        word_b {str} -- word B
        expected {int} -- comparison of values
    """
    received = compare_word(word_a, word_b)

    assert received == expected


@mark.parametrize(
    'kw_a,kw_b,less,equal,reason',
    [
        (gen_inst(1, 2), gen_inst(1, 1), True, False, 's'),
        (gen_inst(1, 2), gen_inst(1, 2), False, True, 's'),
        (gen_inst(1, 2), gen_inst(1, 3), False, False, 's'),
        (gen_inst(1, 2, 'ham'), gen_inst(1, 2), True, False, 'l'),
        (gen_inst(1, 2, 'eggs'), gen_inst(1, 2), True, False, 'l'),
        (gen_inst(1, 2, 'bacon'), gen_inst(1, 2), False, False, 'l'),
        (gen_inst(1, 2, 'spal'), gen_inst(1, 2), True, False, 'w'),
        (gen_inst(1, 2, 'spam'), gen_inst(1, 2), False, True, 'w'),
        (gen_inst(1, 2, 'span'), gen_inst(1, 2), False, False, 'w'), ],
    ids=pad_to_longest([
        'score-lt_b',
        'score-eq_b',
        'score-gt_b',
        'length-lt_b',
        'length-eq_b',
        'length-gt_b',
        'string-lt_b',
        'string-eq_b',
        'string-gt_b', ]))
def test_compare_keywords(
        kw_a: ScoredKeyword,
        kw_b: ScoredKeyword,
        less: bool,
        equal: bool,
        reason: str):
    """Test compare_keywords in parser subpackage

    Arguments:
        kw_a {ScoredKeyword} -- keyword A
        kw_b {ScoredKeyword} -- keyword B
        less {bool} -- A is Less than B
        equal {bool} -- A is Equal to B
    """
    equality = (0, 0, 0)
    received = compare_keywords(kw_a, kw_b)
    assert_msg = 'reason: {}'.format(
        {'s': 'score', 'l': 'length', 'w': 'word'}[reason])

    if less:
        assert received < equality, assert_msg

    elif equal:
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
