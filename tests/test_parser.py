import os.path as path
from pathlib import Path

from oolongt.parser import DEFAULT_LANG, JSON_SUFFIX, Parser
from oolongt.simple_io import load_json

from .helpers import assert_ex, compare_float, compare_dict
from .sample import Sample

BUILTIN = Path(__file__).parent.parent.joinpath('oolongt', 'lang')
DATA_PATH = Path(__file__).parent.joinpath('data')
BASE_LANG_PATH = Path(__file__).parent.joinpath('lang')
TEST_LANG_NAME = 'valid'
TEST_LANG_PATH = BASE_LANG_PATH.joinpath(TEST_LANG_NAME)
TEST_LANG_JSON = TEST_LANG_PATH.joinpath(TEST_LANG_NAME + JSON_SUFFIX)
TEST_LANG_EXPECTED = {
    'meta': {
        'name': 'Valid Language Config'
    },
    'nltk_language': 'valid',
    'ideal': 2,
    'stop_words': 2}
DEFAULT_LANG_EXPECTED = {
    'meta': {
        'name': 'English'
    },
    'nltk_language': 'english',
    'ideal': 20,
    'stop_words': 404}


class TestParser:
    def load_language(self, expected, root=False, lang=False):
        """Load language and compare result with expected

        Arguments:
            expected {Dict} -- expected result

        Keyword Arguments:
            path {str or bool} -- path to language dir (default: {False})
            lang {str or bool} -- language subdirectory (default: {False})
        """
        p = Parser()
        test = False

        samples = [
            # defaults
            (DEFAULT_LANG_EXPECTED, {}),
            # by language
            (DEFAULT_LANG_EXPECTED, {'lang': 'en'}),
            # by path
            (DEFAULT_LANG_EXPECTED, {'root': BUILTIN}),
            # by language and path
            (TEST_LANG_EXPECTED,
                {'lang': TEST_LANG_NAME, 'root': BASE_LANG_PATH}),
            # attempted traversal
            (PermissionError, {'lang': '../../../etc'}),
            # file not found
            (FileNotFoundError, {'root': Path(__file__)}),
            # invalid config
            (ValueError, {'lang': 'malformed', 'root': BASE_LANG_PATH})]

        for sample in samples:
            expected, kwargs = sample

            try:
                result = p.load_language(**kwargs)
                test = compare_dict(expected, result)

            except Exception as e:
                test = isinstance(e, expected)

            assert test, assert_ex('config', result, expected)

    def test_get_all_words(self):
        """Sequential list of the words in text

        Arguments:
            text {str} -- text
            expected {List[str]} -- words
        """
        for sample_name in ['sentence-1word', 'sentence-overlong']:
            samp = Sample(DATA_PATH, sample_name)
            p = Parser()

            expected = samp.d['compare_words']
            for result in p.get_all_words(samp.d['text']):
                assert (result in expected), assert_ex(
                    'all words', result, None)

    def _get_sample_keyword_data(self, samp):
        """Get sample data in Parser.get_keywords() pattern

        Arguments:
            samp {Sample} -- instance of Sample class

        Returns:
            tuple[List[Dict], int] -- result of Parser.get_keywords()
        """
        return (samp.d['keywords'], samp.d['instances'])

    def _get_keyword_result(self, text):
        """Get keywords from Parser

        Arguments:
            text {str} -- text of content

        Returns:
            tuple[List[Dict], int] -- result of Parser.get_keywords()
        """
        p = Parser()
        return p.get_keywords(text)

    def test_get_keywords(self):
        """Test Parser.get_keywords with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        for sample_name in ['empty', 'essay-snark']:
            samp = Sample(DATA_PATH, sample_name)
            text = samp.d['text']

            (expect_kws, expect_insts) = self._get_sample_keyword_data(samp)
            (result_kws, result_insts) = self._get_keyword_result(text)

            assert_ex(
                'total keyword count',
                result_insts,
                expect_insts)

            assert_ex(
                'unique keyword count',
                len(result_kws),
                len(expect_kws))

            unexpected = [
                kw
                for kw in result_kws
                if kw['word'] not in expect_kws.keys()]

            assert (len(unexpected) == 0), assert_ex(
                'keyword present', unexpected, [])

            miscounted = [
                kw
                for kw in result_kws
                if kw['count'] != expect_kws[kw['word']]]

            assert (len(miscounted) == 0), assert_ex(
                'keyword count', miscounted, [])

    def _get_expected_keywords(self, keywords):
        expected = []
        for key in keywords.keys():
            expected += [key] * keywords[key]

        return expected

    def test_get_keyword_list(self):
        sample_name = 'essay-snark'
        samp = Sample(DATA_PATH, sample_name)
        p = Parser(lang=samp.d['lang'])

        expected = sorted(self._get_expected_keywords(samp.d['keywords']))
        result = sorted(p.get_keyword_list(samp.d['text']))

        assert (result == expected), assert_ex(
            'keyword list', expected, result)

    def test_count_keyword(self):
        p = Parser()
        all_words = ['one', 'two', 'three', 'two', 'three', 'three']

        samples = [
            ('zero', 0),
            ('one', 1),
            ('two', 2),
            ('three', 3)]

        for sample in samples:
            unique_word, expected = sample
            result = p.count_keyword(unique_word, all_words)['count']

            assert (result == expected), assert_ex(
                'counting keyword',
                result,
                expected,
                hint=unique_word)

    def test_get_sentence_length_score(self):
        """Test Parser.get_sentence_length_score with
        data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        for sample_name in ['empty',
                            'sentence-short', 'sentence-medium',
                            'sentence-ideal', 'sentence-overlong']:
            samp = Sample(DATA_PATH, sample_name)
            p = Parser(lang=samp.d['lang'])
            words = samp.d['compare_words']

            expected = samp.d['length_score']
            result = p.get_sentence_length_score(words)

            assert compare_float(result, expected), assert_ex(
                'sentence score',
                result,
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
            (0, 10, .17),      # first decile
            (0, 5, .23),       # second decile
            (999, 1000, .15)]  # last sentence

        for sample in samples:
            pos, sentence_count, expected = sample

            p = Parser()
            result = p.get_sentence_position_score(pos, sentence_count)

            assert compare_float(result, expected), assert_ex(
                'sentence position score',
                result,
                expected,
                hint='/'.join([str(pos), str(sentence_count)]))

    def test_get_title_score(self):
        """Test Parser.get_title_score with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        for sample_name in ['sentence-1word', 'sentence-short',
                            'sentence-medium', 'sentence-ideal',
                            'sentence-overlong']:
            samp = Sample(DATA_PATH, sample_name)
            p = Parser(lang=samp.d['lang'])
            title_words = samp.d['compare_title']
            sentence_words = samp.d['compare_words']

            expected = samp.d['title_score']
            result = p.get_title_score(title_words, sentence_words)

            assert compare_float(result, expected), assert_ex(
                'title score',
                result,
                expected,
                hint=[title_words, sentence_words])

    def test_split_sentences(self):
        """Test Parser.split_sentences with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        for sample_name in ['sentence-short', 'sentence-list']:
            samp = Sample(DATA_PATH, sample_name)
            p = Parser(lang=samp.d['lang'])

            expected = samp.d['split_sentences']
            result = p.split_sentences(samp.d['text'])

            assert (result == expected), assert_ex(
                'sentence split',
                result,
                expected)

    def test_split_words(self):
        """Test Parser.split_words with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        for sample_name in ['empty', 'sentence-1word', 'sentence-medium']:
            samp = Sample(DATA_PATH, sample_name)
            p = Parser(lang=samp.d['lang'])
            text = samp.d['text']

            expected = samp.d['split_words']
            result = p.split_words(text)

            assert (result == expected), assert_ex(
                'word split',
                expected,
                result)

    def test_remove_punctuations(self):
        """Test Parser.remove_punctuations with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        for sample_name in ['empty', 'sentence-1word', 'sentence-list']:
            samp = Sample(DATA_PATH, sample_name)
            p = Parser(lang=samp.d['lang'])

            expected = samp.d['remove_punctuations']
            result = p.remove_punctuations(samp.d['text'])

            assert (result == expected), assert_ex(
                'punctuation removal',
                repr(result),
                repr(expected))

    def test_remove_stop_words(self):
        """Test Parser.remove_stop_words with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        for sample_name in ['empty',
                            'sentence-1word', 'sentence-2words',
                            'sentence-list']:
            samp = Sample(DATA_PATH, sample_name)
            p = Parser(lang=samp.d['lang'])
            words = p.split_words(samp.d['text'])

            expected = samp.d['remove_stop_words']
            result = p.remove_stop_words(words)

            assert (result == expected), assert_ex(
                'remove stop words',
                result,
                expected,
                hint=sample_name)
