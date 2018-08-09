""" Test class for Parser """
import os.path as path
import typing

from pytest import mark

from oolongt import roughly
from oolongt.parser import (DEFAULT_LANG, Parser, remove_punctuations,
                            split_words)
from oolongt.simple_io import load_json
from oolongt.typedefs.scored_keyword import ScoredKeyword
from tests.constants import SAMPLES
from tests.helpers import (assert_ex, get_sample_ids, get_samples,
                           pad_to_longest)
from tests.typedefs.sample import Sample
from tests.typedefs.sample_keyword import SampleKeyword


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
def test_split_words(samp: Sample) -> None:
    """Test oolongt.parser.split_words()

    Arguments:
        samp {Sample} -- sample data
    """
    p = Parser()
    text = samp.body

    expected = samp.split_words
    received = split_words(text, p.language)

    assert (received == expected), assert_ex(
        'word split',
        expected,
        received,
        hint=samp.name)


@mark.parametrize(
    'samp',
    get_samples([
        'empty',
        'sentence_1word',
        'sentence_list',
    ]),
    ids=pad_to_longest([
        'empty string',
        'one word',
        'list of sentences',
    ]))
def test_remove_punctuations(samp: Sample) -> None:
    """Test oolongt.parser.remove_punctuations()

    Arguments:
        samp {Sample} -- sample data
    """
    expected = samp.remove_punctuations
    received = remove_punctuations(samp.body)

    assert (received == expected), assert_ex(
        'punctuation removal',
        repr(received),
        repr(expected))


class TestParser:
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
        """Test Parser.get_all_words()

        Arguments:
            samp {Sample} -- sample data
        """
        p = Parser()

        expected = samp.compare_words
        for received in p.get_all_words(samp.body):
            assert (received in expected), assert_ex(
                'all words', received, None)

    def _count_keywords(
            self,
            keywords: typing.List[ScoredKeyword]
            ) -> typing.Tuple[typing.List[str], typing.Dict[str, float]]:
        """Reduce getKeywords() for counting

        Extract word and score properties of keyword list

        Arguments:
            keywords {list[ScoredKeyword]} -- keywords

        Returns:
            typing.Tuple[typing.List[str], typing.Dict[str, float]] --
                return of Parser.get_keywords()
        """
        scores = {}
        words = []

        for kw in keywords:
            word = str(kw)
            scores[word] = kw.score
            words.append(word)

        return words, scores

    def _get_sample_keyword_data(
            self,
            samp: Sample
            ) -> typing.Tuple[typing.List[str], typing.Dict[str, float]]:
        """Get sample data in Parser.get_keywords() pattern

        Arguments:
            samp {Sample} -- sample data

        Returns:
            typing.Tuple[typing.List[str], typing.Dict[str, float]] --
                return of Parser.get_keywords()
        """
        return self._count_keywords(samp.keywords)

    def _get_keyword_result(
            self,
            text: str
            ) -> typing.Tuple[typing.List[str], typing.Dict[str, float]]:
        """Get keywords from Parser

        Arguments:
            text {str} -- body of content

        Returns:
            typing.Tuple[typing.List[str], typing.Dict[str, float]] --
                return of Parser.get_keywords()
        """
        p = Parser()
        keywords = p.get_keywords(text)

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
        """Test Parser.get_keywords()

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
            assert roughly.eq(received, expected), assert_ex(
                'bad keyword score',
                received,
                expected,
                hint=word)

    def _get_expected_keywords(
            self,
            keywords: typing.List[SampleKeyword]
            ) -> typing.List[str]:
        """Get list of expected keywords in text

        Returns:
            list[str] - list of keywords repeated by #occurrences in text
        """
        expected = []  # type: typing.List[str]
        for kw in keywords:
            expected += [kw.word] * kw.count

        return expected

    @mark.parametrize(
        'samp',
        get_samples(['essay_snark'] + SAMPLES),
        ids=get_sample_ids(['essay_snark'] + SAMPLES))
    def test_get_keyword_list(self, samp: Sample) -> None:
        """Test Parser.get_keyword_list()

        Arguments:
            samp {Sample} -- sample data
        """
        p = Parser(lang=samp.lang)

        expected = sorted(self._get_expected_keywords(samp.keywords))
        received = sorted(p.get_keyword_strings(samp.body))

        assert (received == expected), assert_ex(
            'keyword list', expected, received)

    @mark.parametrize(
        'samp',
        get_samples(['sentence_short', 'sentence_list', ] + SAMPLES),
        ids=get_sample_ids(['sentence_short', 'sentence_list', ] + SAMPLES))
    def test_split_sentences(self, samp: Sample) -> None:
        """Test Parser.split_sentences()

        Arguments:
            samp {Sample} -- sample data
        """
        p = Parser(lang=samp.lang)
        expected = None

        try:
            expected = samp.split_sentences

        except AttributeError:
            expected = [sent.text for sent in samp.sentences]

        received = p.split_sentences(samp.body)

        assert (received == expected), assert_ex(
            'sentence split',
            received,
            expected)

    @mark.parametrize(
        'samp',
        get_samples([
            'empty',
            'sentence_1word',
            'sentence_2words',
            'sentence_list',
        ]),
        ids=pad_to_longest([
            'empty string',
            'one word',
            'two words',
            'list of sentences',
        ]))
    def test_remove_stop_words(self, samp: Sample) -> None:
        """Test Parser.remove_stop_words()

        Arguments:
            samp {Sample} -- sample data
        """
        p = Parser(lang=samp.lang)
        words = split_words(samp.body, p.language)

        expected = samp.remove_stop_words
        received = p.remove_stop_words(words)

        assert (received == expected), assert_ex(
            'remove stop words',
            received,
            expected,
            hint=samp.name)
