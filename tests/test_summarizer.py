""" Test class for Summarizer """
from decimal import Decimal
from io import open as io_open
from math import floor
from pathlib import Path
from random import shuffle

from oolongt.nodash import pluck
from oolongt.summarizer import Summarizer

from .assert_ex import assert_ex
from .sample import Sample

DATA_PATH = Path(__file__).parent.joinpath('data')
SAMPLES = ['cambodia', 'cameroon', 'canada']


class TestSummarizer:
    def _compare_float(self, val1, val2):
        """Compare two floating point values

        Arguments:
            val1 {float} -- value 1
            val2 {float} -- value 2

        Returns:
            bool -- the two values are close enough
        """
        return (abs(val1 * 100000 - val2 * 100000) < 2.0)

    def _randomize_list(self, src):
        """Reorder a copy of the supplied list

        Arguments:
            src {list} -- source list

        Returns:
            list -- copy of source list in different order
        """
        dupe = list(src)
        while dupe == src:
            shuffle(dupe)

        return dupe

    def _get_top_keywords(self, keywords):
        """Shadow of Summarizer.get_top_keywords

        keywords should be pre-sorted by frequency

        Arguments:
            keywords {List[Dict]} -- list of keyword Dicts

        Returns:
            List[Dict] -- the ten highest rated keywords
        """
        return [kw for kw in keywords if kw['count'] >= keywords[9]['count']]

    def _get_keyword_list(self, keywords):
        """Get just the words from the keyword Dict

        Arguments:
            keywords {List[Dict]} -- list of keyword Dicts

        Returns:
            List[str] -- list of every value at key 'word'
        """
        return [x['word'] for x in keywords]

    def _snip(self, val, max_len=20, separator=' ', ellip="..."):
        text = val

        if isinstance(val, list):
            text = separator.join(val)

        if len(text) <= max_len:
            return text

        return text[:max_len-len(ellip)] + ellip

    def test_summarize(self):
        """Test Summarizer.summarize() with data from the samples

        Arguments:
            sample_name {str} -- name of data source
        """
        for sample_name in SAMPLES:
            samp = Sample(DATA_PATH, sample_name)
            summ = Summarizer()

            expected = sorted(samp.d['sentences'], key=lambda x: x['rank'])
            results = summ.summarize(
                samp.d['text'], samp.d['title'], None, None)

            assert_ex(
                'summary result count',
                len(results),
                len(expected),
                hint=sample_name)

            for rank, result in enumerate(results):
                assert_ex(
                    'sentence text at rank',
                    result['text'],
                    expected[rank]['text'],
                    hint=[rank, result['text']])

                assert_ex(
                    'sentence order at rank',
                    result['order'],
                    expected[rank]['order'],
                    hint=[rank, result['text']])

    def score_keyword(self, keyword, word_count, expected):
        """Score keyword frequency among other keywords

        Arguments:
            keyword {Dict} -- {count}
            word_count {int} -- total number of keywords
            expected {float} -- expected score
        """
        summ = Summarizer()

        result = summ.score_keyword(keyword, word_count)

        assert_ex(
            'keyword score',
            result['total_score'],
            expected,
            hint=' of '.join([str(keyword['count']), str(word_count)]))

    def test_score_keyword_zero(self):
        keyword = {'count': 0}
        word_count = 1
        expected = 0

        self.score_keyword(keyword, word_count, expected)

    def test_score_keyword_third(self):
        keyword = {'count': 1}
        word_count = 3
        expected = 0.5

        self.score_keyword(keyword, word_count, expected)

    def test_score_keyword_half(self):
        keyword = {'count': 1}
        word_count = 2
        expected = 0.75

        self.score_keyword(keyword, word_count, expected)

    def test_score_keyword_max(self):
        keyword = {'count': 1}
        word_count = 1
        expected = 1.5

        self.score_keyword(keyword, word_count, expected)

    def _test_get_top_keyword_threshold(self, keywords, expected):
        summ = Summarizer()

        result = summ.get_top_keyword_threshold(keywords)

        assert_ex(
            'top keyword frequency >=',
            result,
            expected)

    def test_get_top_keyword_threshold_short(self):
        keywords = [
            {"count": 11},
            {"count": 8},
            {"count": 7},
            {"count": 10},
            {"count": 9},
            {"count": 12}]

        self._test_get_top_keyword_threshold(keywords, 7)

    def test_get_top_keyword_threshold_notie(self):
        keywords = [
            {"count": 2},
            {"count": 4},
            {"count": 7},
            {"count": 1},
            {"count": 8},
            {"count": 5},
            {"count": 12},
            {"count": 9},
            {"count": 11},
            {"count": 6},
            {"count": 10},
            {"count": 3}]

        self._test_get_top_keyword_threshold(keywords, 3)

    def test_get_top_keyword_threshold_tie(self):
        keywords = [
            {"count": 4},
            {"count": 1},
            {"count": 4},
            {"count": 7},
            {"count": 4},
            {"count": 6},
            {"count": 5},
            {"count": 8},
            {"count": 11},
            {"count": 9},
            {"count": 12},
            {"count": 10}]

        self._test_get_top_keyword_threshold(keywords, 4)

    def test_get_top_keywords(self):
        """Test Summarizer.get_top_keywords with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        for sample_name in SAMPLES:
            samp = Sample(DATA_PATH, sample_name)
            summ = Summarizer()

            source = None
            category = None

            keywords = samp.d['keywords']
            expected = self._get_top_keywords(keywords)

            results = summ.get_top_keywords(samp.d['text'], source, category)

            all_keywords = [kw['word'] for kw in keywords]
            assert_ex(
                'result count',
                len(results),
                len(expected))

            for result in results:
                try:
                    idx = all_keywords.index(result['word'])

                    assert_ex(
                        'keyword count',
                        result['count'],
                        keywords[idx]['count'])

                    test = self._compare_float(
                        result['total_score'], keywords[idx]['total_score'])

                    assert_ex(
                        'keyword score',
                        result['total_score'],
                        keywords[idx]['total_score'],
                        test=test)

                except ValueError:
                    assert False, 'keyword error'

    def test_score_sentence(self):
        sentences = []

        for sample_name in SAMPLES:
            samp = Sample(DATA_PATH, sample_name)
            sentences = samp.d['sentences']
            summ = Summarizer()
            title_words = samp.d['title_words']
            top_keywords = self._get_top_keywords(samp.d['keywords'])
            keyword_list = summ._pluck_words(top_keywords)
            num_sents = len(sentences)

            for sentence in sentences:
                idx = sentence['order']
                text = sentence['text']
                expected = sentence['total_score']
                output = summ.score_sentence(
                    idx, text,
                    title_words, top_keywords, keyword_list, num_sents)
                result = output['total_score']

                assert_ex(
                    'sentence score',
                    result,
                    expected,
                    hint=sample_name + ': ' + self._snip(text),
                    test=self._compare_float(result, expected))

    def test_compute_score(self, sample_name):
        """Test Summarizer.computeScore with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        for sample_name in SAMPLES:
            samp = Sample(DATA_PATH, sample_name)
            summ = Summarizer()
            sentences = pluck(samp.d['sentences'], 'text')
            title_words = samp.d['title_words']
            top_keywords = self._get_top_keywords(samp.d['keywords'])

            results = summ.compute_score(sentences, title_words, top_keywords)

            for order, result in enumerate(results):
                expected = samp.d['sentences'][order]
                res_snip = self._snip(result['text'])
                exp_snip = self._snip(expected['text'])

                assert_ex(
                    'sentence order',
                    result['order'],
                    order,
                    hint=[res_snip, exp_snip])

                assert_ex(
                    'sentence score',
                    result['total_score'],
                    expected['total_score'],
                    test=self._compare_float(
                        result['total_score'], expected['total_score']),
                    hint=[res_snip, exp_snip])

                assert_ex(
                    'sentence text',
                    result['text'],
                    expected['text'],
                    hint=[result['text'], expected['text']])

    def _test_sentence_scoring(self, sample_name, score_type):
        """Test Summarizer.sbs or .dbs with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
            score_type  {str} -- score method ('sbs' or 'dbs')
        """
        samp = Sample(DATA_PATH, sample_name)
        summ = Summarizer()

        for sentence in samp.d['sentences']:
            words = summ.parser.get_all_words(sentence['text'])
            top_keywords = self._get_top_keywords(samp.d['keywords'])
            keyword_list = summ._pluck_words(top_keywords)

            expected = sentence[score_type]

            if score_type == 'sbs':
                result = summ.sbs(words, top_keywords, keyword_list)

            if score_type == 'dbs':
                result = summ.dbs(words, top_keywords, keyword_list)

            assert_ex(
                score_type,
                expected,
                result,
                test=self._compare_float(result, expected),
                hint=self._snip(words))

    def sbs(self):
        """Test Summarizer.sbs with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        for sample_name in SAMPLES:
            self._test_sentence_scoring(sample_name, 'sbs')

    def dbs(self, sample_name):
        """Test Summarizer.dbs with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        for sample_name in SAMPLES:
            self._test_sentence_scoring(sample_name, 'dbs')
