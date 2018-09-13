""" Test class for Parser """
import typing

import kinda
from pytest import mark

from src.oolongt.parser.parser import Parser, remove_punctuations
from src.oolongt.parser.scored_keyword import ScoredKeyword
from src.oolongt.typings import StringList
from tests.constants import SAMPLES
from tests.helpers import assert_ex, pad_to_longest
from tests.params.summarizer import get_sample_ids, get_samples
from tests.typings.sample import Sample
from tests.typings.sample_keyword import SampleKeyword

CountedKeywords = typing.Tuple[StringList, typing.Dict[str, float]]


@mark.parametrize(
    'samp',
    get_samples([
        'empty',
        'sentence_1word',
        'sentence_list', ]),
    ids=pad_to_longest([
        'empty string',
        'one word',
        'list of sentences',
    ]))
def test_remove_punctuations(samp: Sample) -> None:
    """Test `remove_punctuations` for Parser

    Arguments:
        samp {Sample} -- sample data
    """
    expected = samp.remove_punctuations
    received = remove_punctuations(samp.body)

    assert (received == expected), assert_ex(
        'punctuation removal',
        repr(received),
        repr(expected))


# pylint: disable=too-few-public-methods,no-self-use
class TestParser:
    """Test `Parser`"""
    @mark.parametrize(
        'samp',
        get_samples([
            'sentence_1word',
            'sentence_overlong',
        ]),
        ids=pad_to_longest([
            'one ',
            'a long sentence',
        ]))
    def test_get_all_words(self, samp: Sample) -> None:
        """Test `Parser.get_all_words`

        Arguments:
            samp {Sample} -- sample data
        """
        parser = Parser()

        expected = samp.compare_words
        for received in parser.get_all_words(samp.body):
            assert (received in expected), assert_ex(
                'all words', received, None)

    @mark.parametrize(
        'samp',
        get_samples(['essay_snark'] + SAMPLES),
        ids=get_sample_ids(['essay_snark'] + SAMPLES))
    def test_get_key_stems(self, samp: Sample) -> None:
        """Test `Parser.get_key_stems`

        Arguments:
            samp {Sample} -- sample data
        """
        parser = Parser(idiom=samp.idiom)

        expected = sorted(self._get_expected_keywords(samp.keywords))
        received = sorted(parser.get_key_stems(samp.body))

        assert (received == expected), assert_ex(
            'keyword list', expected, received)

    def _count_keywords(
            self,
            keywords: typing.List[ScoredKeyword]) -> CountedKeywords:
        """Reduce getKeywords() for counting

        Extract word and score properties of keyword list

        Arguments:
            keywords {typing.List[ScoredKeyword]} -- keywords

        Returns:
            typing.Tuple[StringList, typing.Dict[str, float]] --
                return of Parser.get_keywords()
        """
        scores = {}
        words = []

        for keyword in keywords:
            word = str(keyword)
            scores[word] = keyword.score
            words.append(word)

        return words, scores

    def _get_sample_keyword_data(
            self,
            samp: Sample) -> typing.Tuple[StringList, typing.Dict[str, float]]:
        """Get sample data in `Parser.get_keywords` pattern

        Arguments:
            samp {Sample} -- sample data

        Returns:
            typing.Tuple[StringList, typing.Dict[str, float]] --
                return of `Parser.get_keywords`
        """
        return self._count_keywords(samp.keywords)

    def _get_keyword_result(
            self,
            text: str) -> typing.Tuple[StringList, typing.Dict[str, float]]:
        """Get keywords from Parser

        Arguments:
            text {str} -- body of content

        Returns:
            typing.Tuple[StringList, typing.Dict[str, float]] --
                return of `Parser.get_keywords`
        """
        parser = Parser()
        keywords = parser.get_keywords(text)

        return self._count_keywords(keywords)

    @mark.parametrize(
        'samp',
        get_samples([
            'empty',
            'essay_snark',
        ]),
        ids=pad_to_longest([
            'empty string',
            'Snark essay'
        ]))
    def test_get_keywords(self, samp: Sample) -> None:
        """Test `Parser.get_keywords`

        Arguments:
            samp {Sample} -- sample data
        """
        exp_words, exp_scores = self._get_sample_keyword_data(samp)
        rcv_words, rcv_scores = self._get_keyword_result(samp.body)

        for word in set(exp_words + rcv_words):
            assert (word in exp_words) and (word in rcv_words), assert_ex(
                'word list mismatch',
                rcv_words,
                exp_words)

            expected = exp_scores[word]
            received = rcv_scores[word]
            assert kinda.eq(received, expected), assert_ex(
                'bad keyword score',
                received,
                expected,
                hint=word)

    def _get_expected_keywords(
            self,
            keywords: typing.List[SampleKeyword]) -> StringList:
        """List expected keywords in text

        Returns:
            list[str] - list of keywords repeated by #occurrences in text
        """
        expected = []  # type: StringList
        for keyword in keywords:
            expected += [keyword.word] * keyword.count

        return expected

    @mark.parametrize(
        'samp',
        get_samples(['sentence_short', 'sentence_list', ] + SAMPLES),
        ids=get_sample_ids(['sentence_short', 'sentence_list', ] + SAMPLES))
    def test_split_sentences(self, samp: Sample) -> None:
        """Test `Parser.split_sentences`

        Arguments:
            samp {Sample} -- sample data
        """
        parser = Parser(idiom=samp.idiom)
        expected = None

        try:
            expected = samp.split_sentences

        except AttributeError:
            expected = [sent.text for sent in samp.sentences]

        received = parser.split_sentences(samp.body)

        assert (received == expected), assert_ex(
            'sentence split',
            received,
            expected)

    @mark.parametrize(
        'samp',
        get_samples([
            'empty',
            'sentence_1word',
            'sentence_medium',
        ]),
        ids=pad_to_longest([
            'empty string',
            'one word',
            'medium sentence',
        ]))
    def test_split_words(self, samp: Sample) -> None:
        """Test `Parser.split_words`

        Arguments:
            samp {Sample} -- sample data
        """
        parser = Parser()
        text = samp.body

        expected = samp.split_words
        received = parser.split_words(text)

        assert (received == expected), assert_ex(
            'word split',
            expected,
            received,
            hint=samp.name)
