""" Test class for Summarizer """
from math import floor

from oolongt.nodash import pluck, sort_by
from oolongt.summarizer import Summarizer

from .constants import DATA_PATH, SAMPLES
from .helpers import (
    assert_ex, compare_float, compare_dict, get_samples, randomize_list, snip)
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
        """Test Summarizer.summarize() w/ data from select samples"""
        test_keys = [
            'text',            # 0
            'order',           # 1
            'title_score',     # 2
            'length_score',    # 3
            'position_score',  # 4
            'keyword_score',   # 5
            'keyword_score']   # 6

        for samp in get_samples(*SAMPLES):
            summ = Summarizer()

            expecteds = sort_by(samp.d['sentences'], 'order')
            results = summ.get_sentences(
                samp.d['text'], samp.d['title'], None, None)

            assert (len(results) == len(expecteds)), assert_ex(
                'summary result count',
                len(results),
                len(expecteds),
                hint=samp.name)

            for order, result in enumerate(results):
                expected = expecteds[order]
                test = compare_dict(expected, result, test_keys)

                assert test, assert_ex(
                    'summary',
                    result,
                    expected,
                    hint=[order, snip(results[order]['text'])])

    def test_score_keyword(self):
        """Score keyword frequency among other keywords

        Arguments:
            keyword {Dict} -- {count}
            word_count {int} -- total number of keywords
            expected {float} -- expected score
        """
        #  (appearances of word, total words, expected)
        #               zero|  one third|        half|     maximum|
        samples = [(0, 1, 0), (1, 3, .5), (1, 2, .75), (1, 1, 1.5)]
        summ = Summarizer()

        for sample in samples:
            count, word_count, expected = sample
            keyword = {'count': count}

            result = summ.score_keyword(keyword, word_count)['total_score']

            assert (result == expected), assert_ex(
                'keyword score',
                result['total_score'],
                expected,
                hint=' of '.join([str(keyword['count']), str(word_count)]))

    def _test_get_top_keyword_threshold(self, keywords, expected):
        summ = Summarizer()

        samples = [
            # short
            ([
                {"count": 11},
                {"count": 8},
                {"count": 7},
                {"count": 10},
                {"count": 9},
                {"count": 12}],
                7),
            # no tie
            ([
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
                {"count": 3}],
                3),
            # tied
            ([
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
                {"count": 10}],
                4)]

        for sample in samples:
            keywords, expected = sample

            result = summ.get_top_keyword_threshold(keywords)

            assert (result == expected), assert_ex(
                'top keyword frequency >=',
                result,
                expected)

    def test_get_top_keywords(self):
        """Test Summarizer.get_top_keywords w/ data from select samples"""
        for samp in get_samples(*SAMPLES):
            summ = Summarizer()

            source = None
            category = None

            keywords = samp.d['keywords']
            expected = self._get_top_keywords(keywords)

            results = summ.get_top_keywords(samp.d['text'], source, category)

            all_keywords = [kw['word'] for kw in keywords]
            assert (len(results) == len(expected)), assert_ex(
                'result count',
                len(results),
                len(expected))

            for result in results:
                try:
                    idx = all_keywords.index(result['word'])

                    test = (result['count'] == keywords[idx]['count'])
                    assert test, assert_ex(
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
        for samp in get_samples(*SAMPLES):
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
        """Test Summarizer.score_sentence w/ data from select samples"""
        for samp in get_samples(*SAMPLES):
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
                    hint=[samp.name, snip(text)])

    def test_based_scoring(self):
        """Test Summarizer.dbs and .sbs w/ data from select samples"""
        summ = Summarizer()

        for samp in get_samples(*SAMPLES):
            for sentence in samp.d['sentences']:
                words = summ.parser.get_all_words(sentence['text'])
                top_keywords = self._get_top_keywords(samp.d['keywords'])
                keyword_list = summ._pluck_words(top_keywords)

                for score_type in ['sbs', 'dbs']:
                    expected = sentence[score_type]

                    if score_type == 'dbs':
                        result = summ.dbs(words, top_keywords, keyword_list)

                    if score_type == 'sbs':
                        result = summ.sbs(words, top_keywords, keyword_list)

                    assert compare_float(result, expected), assert_ex(
                        score_type,
                        expected,
                        result,
                        hint=[score_type, snip(words)])
