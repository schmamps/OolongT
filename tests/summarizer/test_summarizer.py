"""Test Summarizer"""
import typing

import kinda
from pytest import mark

from src.oolongt.constants import COMPOSITE_TOLERANCE, TOP_KEYWORD_MIN_RANK
from src.oolongt.summarizer.summarizer import (
    Summarizer, _float_len, get_top_keyword_threshold, pluck_keyword_words,
    score_by_dbs, score_by_sbs, score_by_title)
from src.oolongt.typings import StringList
from tests.constants import SAMPLES
from tests.helpers import assert_ex, pad_to_longest, snip
from tests.params.summarizer import (
    get_sample_ids, get_sample_sentence_ids, get_sample_sentences, get_samples,
    param_threshold)
from tests.typedefs.sample import Sample
from tests.typedefs.sample_keyword import SampleKeyword
from tests.typedefs.sample_sentence import SampleSentence

SampleKeywordList = typing.List[SampleKeyword]


@mark.parametrize(
    'keyword_list,expected',
    [
        (
            [
                SampleKeyword({'word': 'spam'}, 1),
                SampleKeyword({'word': 'eggs'}, 1),
                SampleKeyword({'word': 'bacon'}, 1)
            ],
            ['bacon', 'eggs', 'spam'])],
    ids=pad_to_longest(['spam-eggs']))
def test_pluck_keyword_words(
        keyword_list: SampleKeywordList,
        expected: StringList):
    """Test pluck_keyword_words in summarizer subpackage

    Arguments:
        keyword_list {SampleKeywordList} -- list of ScoredKeywords
        expected {StringList} -- list of word properties
    """
    received = sorted(pluck_keyword_words(keyword_list))

    assert received == expected


@mark.parametrize(
    'item_list,expected',
    [([], 0.0), ([1], 1.0), (range(10), 10.0), (range(10000), 10000.0)],
    ids=pad_to_longest(['    0', '    1', '   10', '10000']))
def test__float_len(item_list: typing.Sized, expected: float):
    """Test _float_len in summarizer subpackage

    Arguments:
        item_list {typing.Sized} -- a sized iterable
        expected {float} -- expected return
    """
    received = _float_len(item_list)

    assert (received == expected), assert_ex(
        'float length',
        received,
        expected)


@param_threshold()
def test_get_top_keyword_threshold(
        keywords: SampleKeywordList,
        expected: float) -> None:
    """Test `Summarizer.get_top_keyword_threshold`

    Arguments:
        keywords {SampleKeywordList} -- sample keywords
        expected {int} -- minimum count
    """
    received = get_top_keyword_threshold(keywords)

    assert (received == expected), assert_ex(
        'top keyword frequency >=',
        received,
        expected)


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
def test_score_by_title(samp: Sample) -> None:
    """Test `Parser.score_by_title`

    Arguments:
        samp {Sample} -- sample data
    """
    summ = Summarizer(idiom=samp.idiom)
    title_words = summ.parser.get_key_words(samp.title)
    sentence_words = summ.parser.get_all_words(samp.sentences[0].text)

    expected = samp.title_score
    received = score_by_title(title_words, sentence_words)

    assert kinda.eq(received, expected), assert_ex(
        'title score',
        received,
        expected,
        hint='\n'.join(['', repr(title_words), repr(sentence_words)]))


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
    top_keywords = summ.get_top_keywords(samp.body)
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
        result = kinda.eq(received, expected, COMPOSITE_TOLERANCE)

        assert result, assert_ex(
            desc,
            received,
            expected)


# pylint: disable=no-self-use
class TestSummarizer:
    """Test Summarizer"""
    def _get_top_keywords(
            self,
            keywords: SampleKeywordList) -> SampleKeywordList:
        """Shadow of `Summarizer.get_top_keywords()`

        keywords should be pre-sorted by frequency

        Arguments:
            keywords {SampleKeywordList} -- list of `SampleKeyword`s

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
        """Test `Summarizer.summarize`

        Arguments:
            samp {Sample} -- sample data
        """
        summ = Summarizer()
        sentences = samp.sentences  # type: typing.List[SampleSentence]

        expecteds = sorted(sentences, key=lambda sent: sent.index)
        receiveds = summ.get_all_sentences(
            samp.body, samp.title)

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
        """Test `Summarizer.get_top_keywords`

        Arguments:
            samp {Sample} -- sample data
        """
        summ = Summarizer()

        expecteds = sorted(
            self._get_top_keywords(samp.keywords))
        exp_len = len(expecteds)

        receiveds = sorted(
            summ.get_top_keywords(samp.body))
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
            sentence: SampleSentence) -> None:
        """Test `Summarizer.get_sentence`

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
        total = len(samp.sentences)

        expected = sentence.total_score
        received = summ.get_sentence(
            text, index, total,
            title_words, top_keywords, top_keyword_list).total_score

        assert kinda.eq(received, expected), assert_ex(
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
        """Test `Summarizer.score_by_length`

        Arguments:
            samp {Sample} -- sample data
        """
        summ = Summarizer(idiom=samp.idiom)
        words = summ.parser.get_all_words(samp.sentences[0].text)

        expected = samp.length_score
        received = summ.score_by_length(words)

        assert kinda.eq(received, expected), assert_ex(
            'sentence score',
            received,
            expected,
            hint=' '.join(words))
