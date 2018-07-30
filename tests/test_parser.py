""" Test class for Parser """
import os.path as path

from pytest import mark

from oolongt import roughly

from oolongt.parser import DEFAULT_LANG, Parser
from oolongt.simple_io import load_json
from tests.constants import SAMPLES
from tests.helpers import assert_ex, get_samples
from tests.typing.sample import Sample


class TestParser:
    @mark.parametrize('samp', get_samples([
        'sentence_1word',
        'sentence_overlong',
    ]))
    def test_get_all_words(self, samp):
        # type: (Sample) -> None
        """Test Parser.get_all_words()

        Arguments:
            samp {Sample} -- sample data
        """
        p = Parser()

        expected = samp.compare_words
        for received in p.get_all_words(samp.body):
            assert (received in expected), assert_ex(
                'all words', received, None)

    def _count_keywords(self, keywords):
        # type: (list[dict], int) -> tuple[list[str], dict[str, float]]
        """Reduce getKeywords() for counting

        TODO: update this docstring

        Arguments:
            keywords {list[dict]} -- keywords

        Returns:
            tuple[list[str], dict[str, float]] - usable data
        """
        scores = {}
        words = []

        for kw in keywords:
            word = kw.word
            scores[word] = kw.score
            words.append(word)

        return words, scores

    def _get_sample_keyword_data(self, samp):
        # type: (Sample) -> list[dict]
        """Get sample data in Parser.get_keywords() pattern

        Arguments:
            samp {Sample} -- sample data

        Returns:
            tuple[list[dict], int] -- return of Parser.get_keywords()
        """
        return self._count_keywords(samp.keywords)

    def _get_keyword_result(self, text):
        # type: (text) -> list[dict]
        """Get keywords from Parser

        Arguments:
            text {str} -- body of content

        Returns:
            tuple[list[dict], int] -- return of Parser.get_keywords()
        """
        p = Parser()
        keywords = p.get_keywords(text)

        return self._count_keywords(keywords)

    @mark.parametrize('samp', get_samples([
        'empty',
        'essay_snark',
    ]))
    def test_get_keywords(self, samp):
        # type: (Sample) -> None
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

    def _get_expected_keywords(self, keywords):
        # type: (list[dict]) -> list[str]
        """Get list of expected keywords in text

        Returns:
            list[str] - list of keywords repeated by #occurrences in text
        """
        expected = []
        for kw in keywords:
            expected += [kw.word] * kw.count

        return expected

    @mark.parametrize('samp', get_samples(['essay_snark'] + SAMPLES))
    def test_get_keyword_list(self, samp):
        # type: (Sample) -> None
        """Test Parser.get_keyword_list()

        Arguments:
            samp {Sample} -- sample data
        """
        p = Parser(lang=samp.lang)

        expected = sorted(self._get_expected_keywords(samp.keywords))
        received = sorted(p.get_keyword_strings(samp.body))

        assert (received == expected), assert_ex(
            'keyword list', expected, received)

    @mark.parametrize('samp', get_samples(
        ['sentence_short', 'sentence_list', ] + SAMPLES
    ))
    def test_split_sentences(self, samp):
        # type: (Sample) -> None
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

    @mark.parametrize('samp', get_samples([
        'empty',
        'sentence_1word',
        'sentence_medium',
    ]))
    def test_split_words(self, samp):
        # type: (Sample) -> None
        """Test Parser.split_words()

        Arguments:
            samp {Sample} -- sample data
        """
        p = Parser(lang=samp.lang)
        text = samp.body

        expected = samp.split_words
        received = p.split_words(text)

        assert (received == expected), assert_ex(
            'word split',
            expected,
            received,
            hint=samp.name)

    @mark.parametrize('samp', get_samples([
        'empty',
        'sentence_1word',
        'sentence_list',
    ]))
    def test_remove_punctuations(self, samp):
        # type: (Sample) -> None
        """Test Parser.remove_punctuations()

        Arguments:
            samp {Sample} -- sample data
        """
        p = Parser(lang=samp.lang)

        expected = samp.remove_punctuations
        received = p.remove_punctuations(samp.body)

        assert (received == expected), assert_ex(
            'punctuation removal',
            repr(received),
            repr(expected))

    @mark.parametrize('samp', get_samples([
        'empty',
        'sentence_1word',
        'sentence_2words',
        'sentence_list',
    ]))
    def test_remove_stop_words(self, samp):
        # type: (Sample) -> None
        """Test Parser.remove_stop_words()

        Arguments:
            samp {Sample} -- sample data
        """
        p = Parser(lang=samp.lang)
        words = p.split_words(samp.body)

        expected = samp.remove_stop_words
        received = p.remove_stop_words(words)

        assert (received == expected), assert_ex(
            'remove stop words',
            received,
            expected,
            hint=samp.name)
