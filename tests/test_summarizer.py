""" Test class for Summarizer """
from math import floor

from pytest import mark

from oolongt import roughly
from oolongt.constants import COMPOSITE_TOLERANCE
from oolongt.summarizer import Summarizer, pluck_keyword_words
from tests.constants import DATA_PATH, SAMPLES
from tests.helpers import (assert_ex, check_exception, get_sample_ids,
                           get_sample_sentence_ids, get_sample_sentences,
                           get_samples, pad_to_longest, randomize_list, snip)
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
        return [kw for kw in keywords if kw.count >= keywords[9].count]

    @mark.parametrize(
        'samp',
        get_samples(SAMPLES),
        ids=pad_to_longest(get_sample_ids(SAMPLES)))
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

    @mark.parametrize(
        'keywords,expected',
        [
            ([
                kbs(.11),
                kbs(.08),
                kbs(.07),
                kbs(.10),
                kbs(.09),
                kbs(.12),
            ], .07),
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
        ],
        ids=pad_to_longest([
            'all pass (count < 10)',
            'simple set (count > 10)',
            'complex (>10 kws ranked <= 10)'
        ]))
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

    @mark.parametrize(
        'samp',
        get_samples(SAMPLES),
        ids=get_sample_ids(SAMPLES))
    def test_get_top_keywords(self, samp):
        # type: (Sample) -> None
        """Test `Summarizer.get_top_keywords()`

        Arguments:
            samp {Sample} -- sample data
        """
        summ = Summarizer()

        source = None
        category = None

        expecteds = sorted(
            self._get_top_keywords(samp.keywords))
        exp_len = len(expecteds)

        receiveds = sorted(
            summ.get_top_keywords(samp.body, source, category))
        rcv_len = len(receiveds)

        assert (rcv_len == exp_len), assert_ex(
            'top keywords count',
            rcv_len,
            exp_len)

        for i, expected in enumerate(expecteds):
            received = receiveds[i]

            assert (received == expected), assert_ex(
                'top keyword',
                received,
                expected)

    @mark.parametrize(
        'samp,sentence',
        get_sample_sentences(SAMPLES),
        ids=get_sample_sentence_ids(SAMPLES))
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
        top_keyword_list = pluck_keyword_words(top_keywords)

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
            result = roughly.eq(received, expected, COMPOSITE_TOLERANCE)

            assert result, assert_ex(
                desc,
                received,
                expected)

    @mark.parametrize(
        'samp,sentence',
        get_sample_sentences(SAMPLES),
        ids=get_sample_sentence_ids(SAMPLES))
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
        top_keyword_list = pluck_keyword_words(top_keywords)
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

    @mark.parametrize(
        'samp',
        get_samples([
            'empty',
            'sentence_short',
            'sentence_medium',
            'sentence_ideal',
            'sentence_overlong',
        ]),
        ids=get_sample_ids([
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

    @mark.parametrize(
        'samp',
        get_samples([
            'sentence_1word',
            'sentence_short',
            'sentence_medium',
            'sentence_ideal',
            'sentence_overlong',
        ]),
        ids=get_sample_ids([
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
