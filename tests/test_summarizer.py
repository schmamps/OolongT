""" Test class for Summarizer """
import typing
from math import floor

from pytest import mark

from oolongt import roughly
from oolongt.constants import COMPOSITE_TOLERANCE, TOP_KEYWORD_MIN_RANK
from oolongt.summarizer import (Summarizer, _float_len,
                                get_top_keyword_threshold, pluck_keyword_words,
                                score_by_dbs, score_by_sbs)
from tests.constants import DATA_PATH, SAMPLES
from tests.helpers import (assert_ex, check_exception, get_sample_ids,
                           get_sample_sentence_ids, get_sample_sentences,
                           get_samples, pad_to_longest, randomize_list, snip)
from tests.typedefs.sample import Sample
from tests.typedefs.sample_keyword import SampleKeyword
from tests.typedefs.sample_sentence import SampleSentence


def kbs(score: float) -> SampleKeyword:
    """Reverse a SampleKeyword from just the score

    Arguments:
        score {float} -- keyword score

    Returns:
        SampleKeyword -- a full-fledged SampleKeyword
    """
    return SampleKeyword.by_score(score)


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
        'all pass (count < minimum rank)',
        'simple set (count > minimum rank)',
        'complex (>MIN_RANK kws ranked <= MIN_RANK)'
    ]))
def test_get_top_keyword_threshold(
        keywords: typing.List[SampleKeyword],
        expected: float
        ) -> None:
    """Test `Summarizer.get_top_keyword_threshold()`

    Arguments:
        keywords {typing.List[SampleKeyword]} -- sample keywords
        expected {int} -- minimum count
    """
    received = get_top_keyword_threshold(keywords)

    assert (received == expected), assert_ex(
        'top keyword frequency >=',
        received,
        expected)


@mark.parametrize(
    'item_list,expected',
    [([], 0.0), ([1], 1.0), (range(10), 10.0), (range(10000), 10000.0)],
    ids=pad_to_longest(['    0', '    1', '   10', '10000']))
def test_float_len(item_list, expected):
    received = _float_len(item_list)

    assert (received == expected), assert_ex(
        'float length',
        received,
        expected)


@mark.parametrize(
    'samp,sentence',
    get_sample_sentences(SAMPLES),
    ids=get_sample_sentence_ids(SAMPLES))
def test_score_frequency(samp: Sample, sentence: SampleSentence) -> None:
    """Test `Summarizer` sentence scoring by keyword frequency

    Arguments:
        samp {Sample} -- sample data
        sentence {SampleSentence} -- individual sentence from sample
    """
    summ = Summarizer()
    words = summ.parser.get_all_stems(sentence.text)
    top_keywords = summ.get_top_keywords(samp.body, None, None)
    top_keyword_list = pluck_keyword_words(top_keywords)

    params = (
        (
            'density score',
            sentence.dbs_score,
            score_by_dbs(words, top_keywords, top_keyword_list),
        ),
        (
            'summation score',
            sentence.sbs_score,
            score_by_sbs(words, top_keywords, top_keyword_list),
        ), )

    for desc, expected, received in params:
        result = roughly.eq(received, expected, COMPOSITE_TOLERANCE)

        assert result, assert_ex(
            desc,
            received,
            expected)


class TestSummarizer:
    def _get_top_keywords(
            self,
            keywords: typing.List[SampleKeyword]
            ) -> typing.List[SampleKeyword]:
        """Shadow of `Summarizer.get_top_keywords()`

        keywords should be pre-sorted by frequency

        Arguments:
            keywords {typing.List[SampleKeyword]} -- list of `SampleKeyword`s

        Returns:
            list[SampleKeyword] -- the ten highest rated keywords
        """
        max_idx = TOP_KEYWORD_MIN_RANK - 1

        return [kw for kw in keywords if kw.count >= keywords[max_idx].count]

    @mark.parametrize(
        'samp',
        get_samples(SAMPLES),
        ids=pad_to_longest(get_sample_ids(SAMPLES)))
    def test_get_all_sentences(self, samp: Sample) -> None:
        """Test `Summarizer.summarize()`

        Arguments:
            samp {Sample} -- sample data
        """
        summ = Summarizer()
        sentences = samp.sentences  # type: typing.List[SampleSentence]

        expecteds = sorted(sentences, key=lambda sent: sent.index)
        receiveds = summ.get_all_sentences(
            samp.body, samp.title, None, None)

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
                hint='{!r}: {!r}'.format(index, snip(receiveds[index].text)))

    @mark.parametrize(
        'samp',
        get_samples(SAMPLES),
        ids=get_sample_ids(SAMPLES))
    def test_get_top_keywords(self, samp: Sample) -> None:
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
    def test_get_sentence(
            self,
            samp: Sample,
            sentence: SampleSentence
            ) -> None:
        """Test `Summarizer.get_sentence()`

        Arguments:
            samp {Sample} -- sample data
            sentence {SampleSentence} -- individual sentence from sample
        """
        summ = Summarizer()
        title_words = samp.title_words
        top_keywords = self._get_top_keywords(samp.keywords)
        top_keyword_list = pluck_keyword_words(top_keywords)
        text = sentence.text
        index = sentence.index
        of = len(samp.sentences)

        expected = sentence.total_score
        received = summ.get_sentence(
            text, index, of,
            title_words, top_keywords, top_keyword_list).total_score

        assert roughly.eq(received, expected), assert_ex(
            'sentence score',
            received,
            expected,
            hint='{}: {!r}'.format(samp.name, snip(text)))

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
    def test_score_by_length(self, samp: Sample) -> None:
        """Test `Summarizer.score_by_length()`

        Arguments:
            samp {Sample} -- sample data
        """
        summ = Summarizer(lang=samp.lang)
        words = summ.parser.get_all_words(samp.sentences[0].text)

        expected = samp.length_score
        received = summ.score_by_length(words)

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
    def test_score_by_title(self, samp: Sample) -> None:
        """Test `Parser.score_by_title()`

        Arguments:
            samp {Sample} -- sample data
        """
        summ = Summarizer(lang=samp.lang)
        title_words = summ.parser.get_key_words(samp.title)
        sentence_words = summ.parser.get_all_words(samp.sentences[0].text)

        expected = samp.title_score
        received = summ.score_by_title(title_words, sentence_words)

        assert roughly.eq(received, expected), assert_ex(
            'title score',
            received,
            expected,
            hint='\n'.join(['', repr(title_words), repr(sentence_words)]))
