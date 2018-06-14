""" Test class for Summarizer """
from math import floor
from pytest import approx

from oolongt.nodash import pluck, sort_by
from oolongt.summarizer import Summarizer

from .constants import DATA_PATH, SAMPLES
from .helpers import (
    assert_ex, compare_dict, get_samples, randomize_list, snip)
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
            'text',
            'order',
            'title_score',
            'length_score',
            'position_score',
            'keyword_score',
            'total_score']

        for samp in get_samples(*SAMPLES):
            summ = Summarizer()

            expecteds = sort_by(samp.d['sentences'], 'order')
            receiveds = summ.get_sentences(
                samp.d['text'], samp.d['title'], None, None)

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

            received = summ.score_keyword(keyword, word_count)['total_score']

            assert (received == expected), assert_ex(
                'keyword score',
                received['total_score'],
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

            received = summ.get_top_keyword_threshold(keywords)

            assert (received == expected), assert_ex(
                'top keyword frequency >=',
                received,
                expected)

    def test_get_top_keywords(self):
        """Test Summarizer.get_top_keywords w/ data from select samples"""
        for samp in get_samples(*SAMPLES):
            summ = Summarizer()

            source = None
            category = None

            keywords = samp.d['keywords']
            expected = self._get_top_keywords(keywords)

            receiveds = summ.get_top_keywords(samp.d['text'], source, category)

            all_keywords = [kw['word'] for kw in keywords]
            assert (len(receiveds) == len(expected)), assert_ex(
                'result count',
                len(receiveds),
                len(expected))

            for received in receiveds:
                try:
                    idx = all_keywords.index(received['word'])

                    test = (received['count'] == keywords[idx]['count'])
                    assert test, assert_ex(
                        'keyword count',
                        received['count'],
                        keywords[idx]['count'])

                    test = approx(
                        received['total_score'], keywords[idx]['total_score'])

                    assert test, assert_ex(
                        'keyword score',
                        received['total_score'],
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
                received = output['total_score']
                test = approx(received, expected)

                assert test, assert_ex(
                    'sentence score',
                    received,
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
                        received = summ.dbs(words, top_keywords, keyword_list)

                    if score_type == 'sbs':
                        received = summ.sbs(words, top_keywords, keyword_list)

                    assert approx(received, expected), assert_ex(
                        score_type,
                        expected,
                        received,
                        hint=[score_type, snip(words)])

    def test_get_sentence_length_score(self):
        """Test Summarizer.get_sentence_length_score
        w/ data from select samples"""

        for samp in get_samples('empty',
                                'sentence_short', 'sentence_medium',
                                'sentence_ideal', 'sentence_overlong'):
            summ = Summarizer(lang=samp.d['lang'])
            words = samp.d['compare_words']

            expected = samp.d['length_score']
            received = summ.get_sentence_length_score(words)

            assert approx(received, expected), assert_ex(
                'sentence score',
                received,
                expected,
                hint=' '.join(words))

    def test_get_sentence_position_score(self):
        """Test Parser.get_sentence_position_score

        Arguments:
            pos {int} -- sentence position (0-based)
            sentence_count {int} -- number of sentences (len())
            expected {float} -- expected score
        """
        samples = [
            (0, 10, .17),               # first decile
            (0, 5, .23),                # second decile
            (999, 1000, .15),           # last sentence
            (999,    0, ValueError),    # out of range
            (999,  999, ValueError), ]  # out of range

        for sample in samples:
            pos, sentence_count, expected = sample

            summ = Summarizer()

            try:
                received = summ.get_sentence_position_score(
                    pos, sentence_count)

                assert approx(received, expected), assert_ex(
                    'sentence position score',
                    received,
                    expected,
                    hint='/'.join([str(pos), str(sentence_count)]))
            except Exception as e:
                assert isinstance(e, expected), assert_ex(
                    'sentence position score',
                    e,
                    expected
                )

    def test_get_title_score(self):
        """Test Parser.get_title_score w/ data from select samples"""
        for samp in get_samples('sentence_1word', 'sentence_short',
                                'sentence_medium', 'sentence_ideal',
                                'sentence_overlong'):
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
