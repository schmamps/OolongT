""" Test class for Summarizer """
from math import floor
from pytest import approx, mark

from oolongt.nodash import pluck, sort_by
from oolongt.summarizer import Summarizer

from .constants import DATA_PATH, SAMPLES
from .helpers import (
    assert_ex, compare_dict,
    get_samples, get_sample_sentences,
    randomize_list, snip, check_exception)
from .sample import Sample

CK = 'count'


class TestSummarizer:
    def _get_top_keywords(self, keywords):
        # type: (list[dict]) -> list[dict]
        """Shadow of `Summarizer.get_top_keywords()`

        keywords should be pre-sorted by frequency

        Arguments:
            keywords {list[dict]} -- list of keyword Dicts

        Returns:
            list[dict] -- the ten highest rated keywords
        """
        return [kw for kw in keywords if kw[CK] >= keywords[9][CK]]

    def _get_keyword_list(self, keywords):
        # type: (list[dict]) -> list[str]
        """Get all values at key 'word' in `keywords`

        Arguments:
            keywords {list[dict]} -- list of keyword Dicts

        Returns:
            list[str] -- all words
        """
        return pluck(keywords, 'word')

    @mark.parametrize('samp', get_samples(SAMPLES))
    def test_get_sentences(self, samp):
        # type: (Sample) -> list[dict]
        """Test `Summarizer.summarize()`

        Arguments:
            samp {Sample} -- sample data
        """
        test_keys = [
            'text',
            'order',
            'title_score',
            'length_score',
            'position_score',
            'keyword_score',
            'total_score']

        summ = Summarizer()

        expecteds = sort_by(samp.d['sentences'], 'order')
        receiveds = summ.get_sentences(
            samp.text, samp.title, None, None)

        assert (len(receiveds) == len(expecteds)), assert_ex(
            'summary result count',
            len(receiveds),
            len(expecteds),
            hint=samp.name)

        for order, received in enumerate(receiveds):
            expected = expecteds[order]
            test = compare_dict(expected, received, test_keys)

            assert test, assert_ex(
                'summary',
                received,
                expected,
                hint=[order, snip(receiveds[order]['text'])])

    @mark.parametrize('count,word_count,expected', [
        (0, 1, 0.00),  # zero
        (1, 3, 0.50),  # one third
        (1, 2, 0.75),  # half
        (1, 1, 1.50),  # maximum
    ])
    def test_score_keyword(self, count, word_count, expected):
        # type: (int, int, float) -> None
        """Test `Summarizer.score_keyword()`

        Arguments:
            count {int} -- {count}
            word_count {int} -- total number of keywords
            expected {float} -- expected score
        """
        summ = Summarizer()
        keyword = {CK: count}

        received = summ.score_keyword(keyword, word_count)['total_score']

        assert (received == expected), assert_ex(
            'keyword score',
            received['total_score'],
            expected,
            hint=' of '.join([str(keyword[CK]), str(word_count)]))

    @mark.parametrize('keywords,expected', [
        # short
        ([{CK: 11}, {CK: 8}, {CK: 7}, {CK: 10}, {CK: 9}, {CK: 12}], 7),
        # no tie
        ([
            {CK: 2},
            {CK: 4},
            {CK: 7},
            {CK: 1},
            {CK: 8},
            {CK: 5},
            {CK: 12},
            {CK: 9},
            {CK: 11},
            {CK: 6},
            {CK: 10},
            {CK: 3},
        ], 3),
        # tied
        ([
            {CK: 4},
            {CK: 1},
            {CK: 4},
            {CK: 7},
            {CK: 4},
            {CK: 6},
            {CK: 5},
            {CK: 8},
            {CK: 11},
            {CK: 9},
            {CK: 12},
            {CK: 10}
        ], 4),
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

    @mark.parametrize('samp', get_samples(SAMPLES))
    def test_get_top_keywords(self, samp):
        # type: (Sample) -> None
        """Test `Summarizer.get_top_keywords()`

        Arguments:
            samp {Sample} -- sample data
        """
        summ = Summarizer()

        source = None
        category = None

        keywords = samp.d['keywords']
        expected = self._get_top_keywords(keywords)

        receiveds = summ.get_top_keywords(samp.text, source, category)

        all_keywords = [kw['word'] for kw in keywords]
        assert (len(receiveds) == len(expected)), assert_ex(
            'result count',
            len(receiveds),
            len(expected))

        for received in receiveds:
            try:
                idx = all_keywords.index(received['word'])

                test = (received[CK] == keywords[idx][CK])
                assert test, assert_ex(
                    'keyword count',
                    received[CK],
                    keywords[idx][CK])

                test = approx(
                    received['total_score'], keywords[idx]['total_score'])

                assert test, assert_ex(
                    'keyword score',
                    received['total_score'],
                    keywords[idx]['total_score'])

            except ValueError:
                assert False, 'keyword error'

    @mark.parametrize('samp,sentence', get_sample_sentences(SAMPLES))
    def test_score_frequency(self, samp, sentence):
        # type: (Sample, dict) -> None
        """Test `Summarizer` sentence scoring by keyword frequency

        Arguments:
            samp {Sample} -- sample data
            sentence {dict} -- individual sentence from sample
        """
        summ = Summarizer()
        top_keywords = summ.get_top_keywords(samp.text, None, None)
        top_keyword_list = summ._pluck_words(top_keywords)

        text = sentence['text']
        words = summ.parser.get_all_words(text)

        expected = (
            sentence['keyword_score'],
            sentence['sbs'],
            sentence['dbs'])
        received = summ.score_frequency(
            words, top_keywords, top_keyword_list)
        hint = [samp.name, snip(text)]

        for inv, desc in enumerate(['DBS', 'SBS', 'keyword score']):
            idx = abs(inv - 2)

            assert approx(expected[idx] == received[idx]), assert_ex(
                desc, received[idx], expected[idx], hint)

    @mark.parametrize('samp,sentence', get_sample_sentences(SAMPLES))
    def test_score_sentence(self, samp, sentence):
        # type: (Sample, dict) -> None
        """Test `Summarizer.score_sentence()`

        Arguments:
            samp {Sample} -- sample data
            sentence {dict} -- individual sentence from sample
        """
        summ = Summarizer()
        title_words = samp.d['title_words']
        top_keywords = self._get_top_keywords(samp.d['keywords'])
        keyword_list = summ._pluck_words(top_keywords)
        num_sents = len(samp.d['sentences'])

        idx = sentence['order']
        text = sentence['text']
        expected = sentence['total_score']
        output = summ.score_sentence(
            idx, text,
            title_words, top_keywords, keyword_list, num_sents)
        received = output['total_score']
        test = approx(received, expected)

        assert test, assert_ex(
            'sentence score',
            received,
            expected,
            hint=[samp.name, snip(text)])

    @mark.parametrize('samp', get_samples([
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
        summ = Summarizer(lang=samp.d['lang'])
        words = samp.d['compare_words']

        expected = samp.d['length_score']
        received = summ.get_sentence_length_score(words)

        assert approx(received, expected), assert_ex(
            'sentence score',
            received,
            expected,
            hint=' '.join(words))

    @mark.parametrize('pos,sentence_count,expected', [
        (0, 10, .17),               # first decile
        (0, 5, .23),                # second decile
        (999, 1000, .15),           # last sentence
        (999,    0, ValueError),    # out of range
        (999,  999, ValueError),    # out of range
    ])
    def test_get_sentence_position_score(self, pos, sentence_count, expected):
        # type: (int, int, float) -> None
        """Test Parser.get_sentence_position_scor()

        Arguments:
            pos {int} -- sentence position (0-based)
            sentence_count {int} -- number of sentences (len())
            expected {float} -- expected score
        """
        summ = Summarizer()
        received = None

        try:
            received = summ.get_sentence_position_score(
                pos, sentence_count)

        except ValueError as e:
            received = check_exception(e, expected)

        assert approx(received, expected), assert_ex(
                'sentence position score',
                received,
                expected,
                hint=' of '.join([str(pos), str(sentence_count)]))

    @mark.parametrize('samp', get_samples([
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
        summ = Summarizer(lang=samp.d['lang'])
        title_words = samp.d['compare_title']
        sentence_words = samp.d['compare_words']

        expected = samp.d['title_score']
        received = summ.get_title_score(title_words, sentence_words)

        assert approx(received, expected), assert_ex(
            'title score',
            received,
            expected,
            hint=[title_words, sentence_words])
