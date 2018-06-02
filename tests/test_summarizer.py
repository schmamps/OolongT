""" Test class for Summarizer """
from math import floor

from oolongt.nodash import pluck, sort_by
from oolongt.summarizer import Summarizer

from .constants import DATA_PATH, SAMPLES
from .helpers import assert_ex, compare_float, randomize_list, snip
from .sample import Sample


class TestSummarizer:
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
        return pluck(keywords, 'word')

    def test_get_sentences(self):
        """Test Summarizer.summarize() with data from the samples

        Arguments:
            sample_name {str} -- name of data source
        """
        test_keys = [
            'text',            # 0
            'order',           # 1
            'title_score',     # 2
            'length_score',    # 3
            'position_score',  # 4
            'keyword_score',   # 5
            'keyword_score']   # 6

        for sample_name in SAMPLES:
            samp = Sample(DATA_PATH, sample_name)
            summ = Summarizer()

            expecteds = sort_by(samp.d['sentences'], 'order')
            results = summ.get_sentences(
                samp.d['text'], samp.d['title'], None, None)

            assert (len(results) == len(expecteds)), assert_ex(
                'summary result count',
                len(results),
                len(expecteds),
                hint=sample_name)

            for order in range(0, len(results)):
                for key in test_keys:
                    expected = expecteds[order][key]
                    result = results[order][key]

                    test = (result == expected)
                    if isinstance(expected, float):
                        test = compare_float(result, expected)

                    assert test, assert_ex(
                        'summary ' + key,
                        result,
                        expected,
                        hint=[order, snip(results[order]['text'])])

    def score_keyword(self, keyword, word_count, expected):
        """Score keyword frequency among other keywords

        Arguments:
            keyword {Dict} -- {count}
            word_count {int} -- total number of keywords
            expected {float} -- expected score
        """
        summ = Summarizer()

        result = summ.score_keyword(keyword, word_count)['total_score']

        assert (result == expected), assert_ex(
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

                    test = compare_float(
                        result['total_score'], keywords[idx]['total_score'])

                    assert test, assert_ex(
                        'keyword score',
                        result['total_score'],
                        keywords[idx]['total_score'])

                except ValueError:
                    assert False, 'keyword error'

    def test_score_frequency(self):
        for sample_name in SAMPLES:
            samp = Sample(DATA_PATH, sample_name)
            sentences = samp.d['sentences']
            summ = Summarizer()
            top_keywords = summ.get_top_keywords(samp.d['text'], None, None)
            top_keyword_list = summ._pluck_words(top_keywords)

            for sentence in sentences:
                text = sentence['text']
                words = summ.parser.get_all_words(text)

                expected = sentence['keyword_score']
                result = summ.score_frequency(
                    words, top_keywords, top_keyword_list)

                assert compare_float(result, expected), assert_ex(
                    'keyword score', result, expected)

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
                test = compare_float(result, expected)

                assert test, assert_ex(
                    'sentence score',
                    result,
                    expected,
                    hint=sample_name + ': ' + snip(text))

    def _test_sentence_score_type(self, sample_name, score_type):
        """Test Summarizer.sbs or .dbs with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
            score_type  {str: 'sbs' or 'dbs'} -- score method
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

            assert compare_float(result, expected), assert_ex(
                score_type,
                expected,
                result,
                hint=snip(words))

    def sbs(self):
        """Test Summarizer.sbs with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        for sample_name in SAMPLES:
            self._test_sentence_score_type(sample_name, 'sbs')

    def dbs(self, sample_name):
        """Test Summarizer.dbs with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        for sample_name in SAMPLES:
            self._test_sentence_score_type(sample_name, 'dbs')
