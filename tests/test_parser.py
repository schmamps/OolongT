""" Test class for Parser """
import os.path as path
from pathlib import Path
from pytest import approx, mark

from oolongt.nodash import pluck
from oolongt.parser import DEFAULT_LANG, JSON_SUFFIX, Parser
from oolongt.simple_io import load_json

from .constants import SAMPLES
from .helpers import assert_ex, compare_dict, get_samples, check_exception
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
    def _compare_loaded_language(self, received, expected):
        """Compare loaded language data to expected

        Arguments:
            received {dict} -- received data
            expected {dict} -- expected data

        Raises:
            ValueError -- Wrong data
        """
        if not (len(received['stop_words']) == expected['stop_words']):
            raise ValueError('stop word mismatch')

        if not compare_dict(expected, received, ignore=['stop_words']):
            raise ValueError('wrong language data loaded')

        return True

    @mark.parametrize(
        'expected,kwargs',
        [
            # defaults
            [DEFAULT_LANG_EXPECTED, {}],
            # by language
            [DEFAULT_LANG_EXPECTED, {'lang': 'en'}],
            # by path
            [DEFAULT_LANG_EXPECTED, {'root': BUILTIN}],
            # by language and path
            [TEST_LANG_EXPECTED,
                {'lang': TEST_LANG_NAME, 'root': BASE_LANG_PATH}],
            # attempted traversal
            [PermissionError, {'lang': '../../../etc'}],
            # file not found
            [FileNotFoundError, {'root': Path(__file__)}],
            # invalid config
            [ValueError, {'lang': 'malformed', 'root': BASE_LANG_PATH}],
        ]
    )
    def test_load_language(self, expected, kwargs):
        """Test Parser.load_language()

        Arguments:
            expected {dict} -- expected received
            kwargs {dict} -- kwargs passed to Parser
        """
        p = Parser()
        test = False

        try:
            received = p.load_language(**kwargs)
            test = self._compare_loaded_language(received, expected)

        except (PermissionError, FileNotFoundError, ValueError) as e:
            test = check_exception(e, expected) is not None

        assert test, assert_ex('config', received, expected)

    @mark.parametrize('samp', get_samples([
        'sentence_1word',
        'sentence_overlong',
    ]))
    def test_get_all_words(self, samp):
        """Test Parser.get_all_words()

        Arguments:
            samp {Sample} -- sample data
        """
        p = Parser()

        expected = samp.d['compare_words']
        for received in p.get_all_words(samp.text):
            assert (received in expected), assert_ex(
                'all words', received, None)

    def _count_keywords(self, keywords, insts):
        """Reduce getKeywords() for counting

        TODO: update this docstring

        Arguments:
            keywords {list[dict]} -- keywords
            insts {int} -- instances

        Returns:
            dict[counts: dict, words: list[str], total: int] - usable data
        """
        counts = {}
        words = []

        for kw in keywords:
            word = kw['word']
            counts[word] = kw['count']
            words.append(word)

        return {'counts': counts, 'words': words, 'total': insts}

    def _get_sample_keyword_data(self, samp):
        """Get sample data in Parser.get_keywords() pattern

        Arguments:
            samp {Sample} -- sample data

        Returns:
            tuple[list[dict], int] -- return of Parser.get_keywords()
        """
        keywords = samp.d['keywords']
        insts = samp.d['instances']

        return self._count_keywords(keywords, insts)

    def _get_keyword_result(self, text):
        """Get keywords from Parser

        Arguments:
            text {str} -- body of content

        Returns:
            tuple[list[dict], int] -- return of Parser.get_keywords()
        """
        p = Parser()
        keywords, insts = p.get_keywords(text)

        return self._count_keywords(keywords, insts)

    @mark.parametrize('samp', get_samples([
        'empty',
        'essay_snark',
    ]))
    def test_get_keywords(self, samp):
        """Test Parser.get_keywords()

        Arguments:
            samp {Sample} -- sample data
        """
        expected = self._get_sample_keyword_data(samp)
        received = self._get_keyword_result(samp.text)

        assert (received['total'] == expected['total']), assert_ex(
            'total keyword count',
            received['total'],
            expected['total'])

        for word in set(expected['words'] + received['words']):
            assert word in expected['words'], assert_ex(
                'unexpected word received',
                word,
                None)

            assert word in received['words'], assert_ex(
                'expected word not received',
                word,
                None)

            exp_count = expected['counts'][word]
            rcv_count = received['counts'][word]
            assert exp_count == rcv_count, assert_ex(
                'bad keyword count',
                rcv_count,
                exp_count,
                hint=word)

    def _get_expected_keywords(self, keywords):
        """Get list of expected keywords in text

        Returns:
            list[str] - list of keywords repeated by #occurrences in text
        """
        expected = []
        for kw in keywords:
            expected += [kw['word']] * kw['count']

        return expected

    @mark.parametrize('samp', get_samples(['essay_snark'] + SAMPLES))
    def test_get_keyword_list(self, samp):
        """Test Parser.get_keyword_list()

        Arguments:
            samp {Sample} -- sample data
        """
        p = Parser(lang=samp.d['lang'])

        expected = sorted(self._get_expected_keywords(samp.d['keywords']))
        received = sorted(p.get_keyword_list(samp.text))

        assert (received == expected), assert_ex(
            'keyword list', expected, received)

    @mark.parametrize('samp', [
        ('zero', 0),
        ('one', 1),
        ('two', 2),
        ('three', 3),
    ])
    def test_count_keyword(self, samp):
        """Test Parser.count_keyword()

        Arguments:
            samp {Tuple[str, int]} -- search string, count
        """
        p = Parser()
        all_words = ['one', 'two', 'three', 'two', 'three', 'three']

        unique_word, expected = samp
        received = p.count_keyword(unique_word, all_words)['count']

        assert (received == expected), assert_ex(
            'counting keyword',
            received,
            expected,
            hint=unique_word)

    @mark.parametrize('samp', get_samples(
        ['sentence_short', 'sentence_list', ] + SAMPLES
    ))
    def test_split_sentences(self, samp):
        """Test Parser.split_sentences()

        Arguments:
            samp {Sample} -- sample data
        """
        DEFAULT_KEY = 'split_sentences'
        p = Parser(lang=samp.d['lang'])

        if DEFAULT_KEY in samp.d.keys():
            expected = samp.d[DEFAULT_KEY]
        else:
            expected = pluck(samp.d['sentences'], 'text')

        received = p.split_sentences(samp.text)

        assert (received == expected), assert_ex(
            'sentence split',
            received,
            expected)

    @mark.parametrize('samp', get_samples([
        'empty',
        'sentence_1word',
        'sentence_medium',
    ]))
    def test_split_words(self, samp):
        """Test Parser.split_words()

        Arguments:
            samp {Sample} -- sample data
        """

        p = Parser(lang=samp.d['lang'])
        text = samp.text

        expected = samp.d['split_words']
        received = p.split_words(text)

        assert (received == expected), assert_ex(
            'word split',
            expected,
            received,
            hint=samp.name)

    @mark.parametrize('samp', get_samples([
        'empty',
        'sentence_1word',
        'sentence_list',
    ]))
    def test_remove_punctuations(self, samp):
        """Test Parser.remove_punctuations()

        Arguments:
            samp {Sample} -- sample data
        """
        p = Parser(lang=samp.d['lang'])

        expected = samp.d['remove_punctuations']
        received = p.remove_punctuations(samp.text)

        assert (received == expected), assert_ex(
            'punctuation removal',
            repr(received),
            repr(expected))

    @mark.parametrize('samp', get_samples([
        'empty',
        'sentence_1word',
        'sentence_2words',
        'sentence_list',
    ]))
    def test_remove_stop_words(self, samp):
        """Test Parser.remove_stop_words()

        Arguments:
            samp {Sample} -- sample data
        """
        p = Parser(lang=samp.d['lang'])
        words = p.split_words(samp.text)

        expected = samp.d['remove_stop_words']
        received = p.remove_stop_words(words)

        assert (received == expected), assert_ex(
            'remove stop words',
            received,
            expected,
            hint=samp.name)
