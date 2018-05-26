""" Test class for Summarizer """
from math import floor
from pathlib import Path
from random import shuffle
from textteaser.summarizer import Summarizer
from textteaser.nodash import pluck
from .assert_ex import assert_ex
from .sample import Sample

DATA_PATH = Path(__file__).parent.joinpath('data')


class TestSummarizer:
    def _compareFloat(self, val1, val2):
        """Compare two floating point values

        Arguments:
            val1 {float} -- value 1
            val2 {float} -- value 2

        Returns:
            bool -- the two values are close enough
        """
        return (int(val1 * 100000) - int(val2 * 100000) < 2)

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
        """Shadow of Summarizer.getTopKeywords

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

    def summarize(self, sample_name):
        """Test Summarizer.summarize() with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        samp = Sample(DATA_PATH, sample_name)
        summ = Summarizer()

        expected = sorted(samp.d['sentences'], key=lambda x: x['rank'])
        results = summ.summarize(samp.d['text'], samp.d['title'], None, None)

        assert_ex(
            'summary result count',
            len(results),
            len(expected),
            hint=sample_name)

        for rank, result in enumerate(results):
            assert_ex(
                'sentence text at rank',
                result['sentence'],
                expected[rank]['text'],
                hint=[rank, result['sentence']])

            assert_ex(
                'sentence order at rank',
                result['order'],
                expected[rank]['order'],
                hint=[rank, result['sentence']])

    def test_summarize_cambodia(self):
        self.summarize('cambodia')

    def test_summarize_cameroon(self):
        self.summarize('cameroon')

    def test_summarize_canada(self):
        self.summarize('canada')

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
            result['totalScore'],
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

    def _test_get_top_keywords(self, sample_name):
        """Test Summarizer.getTopKeywords with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
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

                test = self._compareFloat(
                    result['totalScore'], keywords[idx]['totalScore'])

                assert_ex(
                    'keyword score',
                    result['totalScore'],
                    keywords[idx]['totalScore'],
                    test=test)

            except ValueError:
                assert False, 'keyword error'

    def test_get_top_keywords_cambodia(self):
        self._test_get_top_keywords('cambodia')

    def test_get_top_keywords_cameroon(self):
        self._test_get_top_keywords('cameroon')

    def test_get_top_keywords_canada(self):
        self._test_get_top_keywords('canada')

    def _test_sortScore(self, sample_name):
        """Test Summarizer.sortScore with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        samp = Sample(DATA_PATH, sample_name)
        summ = Summarizer()
        sentences = self._randomize_list(samp.d['sentences'])

        results = summ.sortScore(sentences)

        for result in results:
            try:
                expected = [
                    x for x in sentences
                    if x['order'] == result['order']][0]

                rv = result['totalScore']
                ev = expected['totalScore']
                cv = self._compareFloat(rv, ev)

                assert_ex('sort score', rv, ev, test=cv)

            except IndexError:
                assert False, 'bad sentence list'

    def test_sortScore_cambodia(self):
        self._test_sortScore('cambodia')

    def test_sortScore_cameroon(self):
        self._test_sortScore('cameroon')

    def test_sortScore_canada(self):
        self._test_sortScore('canada')

    def _test_sortSentences(self, sample_name):
        """Test Summarizer.sortSentences with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        samp = Sample(DATA_PATH, sample_name)
        summ = Summarizer()
        sentences = self._randomize_list(samp.d['sentences'])

        results = summ.sortSentences(sentences)

        for expected, result in enumerate(results):
            assert_ex('sort order', result['order'], expected)

    def test_sortSentences_cambodia(self):
        self._test_sortSentences('cambodia')

    def test_sortSentences_cameroon(self):
        self._test_sortSentences('cameroon')

    def test_sortSentences_canada(self):
        self._test_sortSentences('canada')

    def computeScore(self, sample_name):
        """Test Summarizer.computeScore with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        samp = Sample(DATA_PATH, sample_name)
        summ = Summarizer()
        sentences = pluck(samp.d['sentences'], 'text')
        title_words = samp.d['titleWords']
        top_keywords = self._get_top_keywords(samp.d['keywords'])

        results = summ.computeScore(sentences, title_words, top_keywords)

        for order, result in enumerate(results):
            expected = samp.d['sentences'][order]
            res_snip = result['sentence'][:17] + '...'
            exp_snip = expected['text'][:17] + '...'

            assert_ex(
                'sentence order',
                result['order'],
                order,
                hint=[res_snip, exp_snip])

            assert_ex(
                'sentence score',
                result['totalScore'],
                expected['totalScore'],
                test=self._compareFloat(
                    result['totalScore'], expected['totalScore']),
                hint=[res_snip, exp_snip])

            assert_ex(
                'sentence text',
                result['sentence'],
                expected['text'],
                hint=[result['sentence'], expected['text']])

    def test_computeScore_cambodia(self):
        self.computeScore('cambodia')

    def test_computeScore_cameroon(self):
        self.computeScore('cameroon')

    def test_computeScore_canada(self):
        self.computeScore('canada')

    def _test_sentence_scoring(self, sample_name, score_type):
        """Test Summarizer.sbs or .dbs with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
            score_type  {str} -- score method ('sbs' or 'dbs')
        """
        samp = Sample(DATA_PATH, sample_name)
        summ = Summarizer()

        for sentence in samp.d['sentences']:
            unpunct = summ.parser.removePunctations(sentence)
            words = summ.parser.splitWords(unpunct)
            topKeywords = self._get_top_keywords(samp.d['keywords'])
            keywordList = self._get_keyword_list(samp.d['keywords'])

            expected = sentence[score_type]

            if score_type == 'sbs':
                result = summ.sbs(words, topKeywords, keywordList)

            if score_type == 'dbs':
                result = summ.dbs(words, topKeywords, keywordList)

            assert_ex(
                score_type,
                expected,
                result,
                test=self._compareFloat(result, expected),
                hint=unpunct)

    def sbs(self, sample_name):
        """Test Summarizer.sbs with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        self._test_sentence_scoring(sample_name, 'sbs')

    def test_sbs_cambodia(self):
        self.sbs('cambodia')

    def test_sbs_cameroon(self):
        self.sbs('cameroon')

    def test_sbs_canada(self):
        self.sbs('canada')

    def dbs(self, sample_name):
        """Test Summarizer.dbs with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        self._test_sentence_scoring(sample_name, 'dbs')

    def test_dbs_cambodia(self):
        self.dbs('cambodia')

    def test_dbs_cameroon(self):
        self.dbs('cameroon')

    def test_dbs_canada(self):
        self.dbs('canada')
