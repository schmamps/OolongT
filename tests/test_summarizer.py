""" Test class for Summarizer """
from math import floor

import pytest

from oolongt import roughly

from oolongt.nodash import pluck, sort_by
from oolongt.summarizer import Summarizer
from tests.constants import DATA_PATH, SAMPLES
from tests.helpers import (assert_ex, check_exception,
                           get_sample_sentences, get_samples, randomize_list,
                           snip)
from tests.typing.sample import Sample
from tests.typing.sample_keyword import SampleKeyword


def kbs(score):
    return SampleKeyword.by_score(score)


class TestSummarizer:
    def _get_top_keywords(self, keywords):
        # type: (list[dict]) -> list[SampleKeyword]
        """Shadow of `Summarizer.get_top_keywords()`

        keywords should be pre-sorted by frequency

        Arguments:
            keywords {list[dict]} -- list of keyword Dicts

        Returns:
            list[SampleKeyword] -- the ten highest rated keywords
        """
        return [kw for kw in keywords if kw.score >= keywords[9].score]

    @pytest.mark.parametrize('samp', get_samples(SAMPLES))
    def test_get_sentences(self, samp):
        # type: (Sample) -> list[dict]
        """Test `Summarizer.summarize()`

        Arguments:
            samp {Sample} -- sample data
        """
        summ = Summarizer()
        sentences = samp.sentences  # type: list[SampleSentence]

        expecteds = sorted(sentences, key=lambda sent: sent.index)
        receiveds = summ.get_sentences(samp.body, samp.title, None, None)

        assert (len(receiveds) == len(expecteds)), assert_ex(
            'summary result count',
            len(receiveds),
            len(expecteds),
            hint=samp.name)

        for index, received in enumerate(receiveds):
            expected = expecteds[index]  # type: SampleSentence

            assert expected.equals(received), assert_ex(
                'summary',
                received,
                expected,
                hint=[index, snip(receiveds[index].text)])

    @pytest.mark.parametrize('keywords,expected', [
        # short
        ([
            kbs(.11),
            kbs(.08),
            kbs(.07),
            kbs(.10),
            kbs(.09),
            kbs(.12),
        ], .07),
        # no tie
        ([
            kbs(.02),
            kbs(.04),
            kbs(.07),
            kbs(.01),
            kbs(.08),
            kbs(.05),
            kbs(.12),
            kbs(.09),
            kbs(.11),
            kbs(.06),
            kbs(.10),
            kbs(.03),
        ], .03),
        # tied
        ([
            kbs(.04),
            kbs(.01),
            kbs(.04),
            kbs(.07),
            kbs(.04),
            kbs(.06),
            kbs(.05),
            kbs(.08),
            kbs(.11),
            kbs(.09),
            kbs(.12),
            kbs(.10),
        ], .04),
    ])
    def test_get_top_keyword_threshold(self, keywords, expected):
        # type: (list[dict], int) - None
        """Test `Summarizer.get_top_keyword_threshold()`

        Arguments:
            keywords {list[dict]} -- Dicts with 'count' key
            expected {int} -- minimum count
        """
        summ = Summarizer()

        received = summ.get_top_keyword_threshold(keywords)

        assert (received == expected), assert_ex(
            'top keyword frequency >=',
            received,
            expected)

    @pytest.mark.parametrize('samp', get_samples(SAMPLES))
    def test_get_top_keywords(self, samp):
        # type: (Sample) -> None
        """Test `Summarizer.get_top_keywords()`

        Arguments:
            samp {Sample} -- sample data
        """
        summ = Summarizer()

        source = None
        category = None

        keywords = samp.keywords
        expected = self._get_top_keywords(keywords)

        receiveds = summ.get_top_keywords(samp.body, source, category)

        all_keywords = summ._pluck_words(keywords)
        assert (len(receiveds) == len(expected)), assert_ex(
            'result count',
            len(receiveds),
            len(expected))

        for received in receiveds:
            try:
                idx = all_keywords.index(received.word)

                test = roughly.eq(received.score, keywords[idx].score)
                assert test, assert_ex(
                    'keyword score',
                    received.score,
                    keywords[idx].score)

            except ValueError:
                assert False, 'keyword error'

    @pytest.mark.parametrize('samp,sentence', get_sample_sentences(SAMPLES))
    def test_score_frequency(self, samp, sentence):
        # type: (Sample, dict) -> None
        """Test `Summarizer` sentence scoring by keyword frequency

        Arguments:
            samp {Sample} -- sample data
            sentence {dict} -- individual sentence from sample
        """
        summ = Summarizer()
        words = summ.parser.get_all_words(sentence.text)
        top_keywords = summ.get_top_keywords(samp.body, None, None)
        top_keyword_list = summ._pluck_words(top_keywords)

        params = (
            (
                'density score',
                sentence.dbs_score,
                summ.score_dbs(words, top_keywords, top_keyword_list),
            ),
            (
                'summation score',
                sentence.sbs_score,
                summ.score_sbs(words, top_keywords, top_keyword_list),
            ), )

        for desc, expected, received in params:
            assert roughly.eq(received, expected), assert_ex(
                desc,
                received,
                expected)

    @pytest.mark.parametrize('samp,sentence', get_sample_sentences(SAMPLES))
    def test_score_sentence(self, samp, sentence):
        # type: (Sample, dict) -> None
        """Test `Summarizer.score_sentence()`

        Arguments:
            samp {Sample} -- sample data
            sentence {dict} -- individual sentence from sample
        """
        summ = Summarizer()
        title_words = samp.title_words
        top_keywords = self._get_top_keywords(samp.keywords)
        top_keyword_list = summ._pluck_words(top_keywords)
        text = sentence.text
        index = sentence.index
        of = len(samp.sentences)

        expected = sentence.total_score
        received = summ.get_scored_sentence(
            text, index, of,
            title_words, top_keywords, top_keyword_list).total_score

        assert roughly.eq(received, expected), assert_ex(
            'sentence score',
            received,
            expected,
            hint=[samp.name, snip(text)])

    @pytest.mark.parametrize('samp', get_samples([
        'empty',
        'sentence_short',
        'sentence_medium',
        'sentence_ideal',
        'sentence_overlong',
    ]))
    def test_get_sentence_length_score(self, samp):
        # type: (Sample) -> None
        """Test `Summarizer.get_sentence_length_score()`

        Arguments:
            samp {Sample} -- sample data
        """
        summ = Summarizer(lang=samp.lang)
        words = samp.compare_words

        expected = samp.length_score
        received = summ.score_sentence_length(words)

        assert roughly.eq(received, expected), assert_ex(
            'sentence score',
            received,
            expected,
            hint=' '.join(words))

    @pytest.mark.parametrize('samp', get_samples([
        'sentence_1word',
        'sentence_short',
        'sentence_medium',
        'sentence_ideal',
        'sentence_overlong',
    ]))
    def test_get_title_score(self, samp):
        # type: (Sample) -> None
        """Test `Parser.get_title_score()`

        Arguments:
            samp {Sample} -- sample data
        """
        summ = Summarizer(lang=samp.lang)
        title_words = samp.compare_title
        sentence_words = samp.compare_words

        expected = samp.title_score
        received = summ.score_title(title_words, sentence_words)

        assert roughly.eq(received, expected), assert_ex(
            'title score',
            received,
            expected,
            hint=[title_words, sentence_words])
