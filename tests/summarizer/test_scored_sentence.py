"""Test `ScoredSentence`"""
from src.oolongt.summarizer.scored_sentence import ScoredSentence
from tests.params.summarizer import (
    get_inst_comp, param_comp,
    param_scored_sentence___init__,
    param_scored_sentence__repr__, param_scored_sentence__str__,
    instantiate_scored_sentence as instantiate)


# pylint: disable=no-self-use
class TestScoredSentence:
    """Test `ScoredSentence`"""
    @param_scored_sentence___init__()
    def test___init__(self, init: list, expected: list):
        """Test `ScoredSentence` initialization

        Arguments:
            init {list} -- initialization parameters
            expected {list} -- expected property values
        """
        inst = instantiate(init)
        received = get_inst_comp(inst)

        assert received == expected

    @param_scored_sentence__str__()
    def test___str__(self, init: list, expected: str):
        """Test `ScoredSentence` string cast

        Arguments:
            init {list} -- initialization parameters
            expected {str} -- expected value
        """
        inst = instantiate(init)
        received = str(inst)

        assert received == expected

    @param_scored_sentence__repr__()
    def test___repr__(self, init: list, expected: str):
        """Test `ScoredSentence` REPR

        Arguments:
            init {list} -- initialization parameters
            expected {str} -- expected value
        """
        inst = instantiate(init)
        received = repr(inst)

        assert received.replace("'", '"') == expected

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
