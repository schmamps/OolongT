from textteaser.parser \
    import Parser, DEFAULT_LANG, JSON_SUFFIX, TOKEN_SUFFIX
from textteaser.simple_io \
    import load_json
import os.path as path
from pathlib import Path
from .sample import Sample
from .assert_ex import assert_ex

BUILTIN = Path(__file__).parent.parent.joinpath('textteaser', 'lang')
DATA_PATH = Path(__file__).parent.joinpath('data')
BASE_LANG_PATH = Path(__file__).parent.joinpath('lang')
TEST_LANG_NAME = 'valid'
TEST_LANG_PATH = BASE_LANG_PATH.joinpath(TEST_LANG_NAME)
TEST_LANG_JSON = TEST_LANG_PATH.joinpath(TEST_LANG_NAME + JSON_SUFFIX)
TEST_LANG_TOKEN = TEST_LANG_PATH.joinpath(TEST_LANG_NAME + TOKEN_SUFFIX)
TEST_LANG_EXPECTED = {
    'meta': {
        'name': 'Valid Language Config'
    },
    'ideal': 2,
    'stop_words': 2,
    'token_path': TEST_LANG_TOKEN}
DEFAULT_LANG_EXPECTED = {
    'meta': {
        'name': 'English'
    },
    'ideal': 20,
    'stop_words': 404,
    'token_path': BUILTIN.joinpath(
        DEFAULT_LANG, DEFAULT_LANG + TOKEN_SUFFIX)}


class TestParser:
    def _test_load_language(self, expected, path=False, lang=False):
        """Load language and compare result with expected

        Arguments:
            expected {Dict} -- expected result

        Keyword Arguments:
            path {str or bool} -- path to language dir (default: {False})
            lang {str or bool} -- language subdirectory (default: {False})
        """
        parser = Parser()

        result = parser.load_language(path or BUILTIN, lang or DEFAULT_LANG)
        result['stop_words'] = len(result['stop_words'])

        for key in expected.keys():
            assert_ex('config: ' + key, str(result[key]), str(expected[key]))

    def _test_load_language_error(self, expected, path=False, lang=False):
        """Load language and await an exception

        Arguments:
            expected {any} -- try: ... except (expected):

        Keyword Arguments:
            path {str or bool} -- path to language dir (default: {False})
            lang {str or bool} -- language subdirectory (default: {False})
        """
        parser = Parser()

        result = False

        try:
            parser.load_language(
                path=path or BUILTIN, lang=lang or DEFAULT_LANG)

        except Exception as e:
            result = isinstance(e, expected)

        assert result, 'expected throw(s): ' + str(expected)

    def test_load_language_default(self):
        self._test_load_language(DEFAULT_LANG_EXPECTED)

    def test_load_language_by_lang(self):
        self._test_load_language(DEFAULT_LANG_EXPECTED, lang='en')

    def test_load_language_by_path(self):
        self._test_load_language(DEFAULT_LANG_EXPECTED, path=BUILTIN)

    def test_load_language_by_all(self):
        self._test_load_language(
            TEST_LANG_EXPECTED, lang=TEST_LANG_NAME, path=BASE_LANG_PATH)

    def test_load_language_traversal(self):
        self._test_load_language_error(PermissionError, lang='../../../etc')

    def test_load_language_notfound(self):
        path = Path(__file__)
        self._test_load_language_error(FileNotFoundError, path=path)

    def test_load_language_malformed(self):
        self._test_load_language_error(
            ValueError, lang='malformed', path=BASE_LANG_PATH)

    def test_load_language_empty(self):
        self._test_load_language_error(
            FileNotFoundError, lang='nonexistent', path=BASE_LANG_PATH)

    def _get_sample_keyword_data(self, samp):
        """Get sample data in Parser.getKeywords() pattern

        Arguments:
            samp {Sample} -- instance of Sample class

        Returns:
            tuple[List[Dict], int] -- result of Parser.getKeywords()
        """
        return (samp.d['keywords'], samp.d['instances'])

    def _get_keyword_result(self, text):
        """Get keywords from Parser

        Arguments:
            text {str} -- text of content

        Returns:
            tuple[List[Dict], int] -- result of Parser.getKeywords()
        """
        parser = Parser()
        return parser.getKeywords(text)

    def _test_getKeywords(self, sample_name):
        """Test Parser.getKeywords with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
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

        assert_ex(
            'keyword present', unexpected, [], test=len(unexpected) == 0)

        miscounted = [
            kw
            for kw in result_kws
            if kw['count'] != expect_kws[kw['word']]]

        assert_ex(
            'keyword count', miscounted, [], test=len(miscounted) == 0)

    def test_getKeywords_empty(self):
        self._test_getKeywords('empty')

    def test_getKeywords_essay(self):
        self._test_getKeywords('essay-snark')

    def _test_getSentenceLengthScore(self, sample_name):
        """Test Parser.getSentenceLengthScore with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        samp = Sample(DATA_PATH, sample_name)
        parser = Parser(lang=samp.d['lang'])
        words = samp.d['compareWords']

        expected = samp.d['lengthScore']
        result = parser.getSentenceLengthScore(words)

        assert_ex(
            'sentence score',
            result,
            expected,
            hint=' '.join(words))

    def test_getSentenceLengthScore_empty(self):
        self._test_getSentenceLengthScore('empty')

    def test_getSentenceLengthScore_qtr_ideal(self):
        self._test_getSentenceLengthScore('sentence-short')

    def test_getSentenceLengthScore_half_ideal(self):
        self._test_getSentenceLengthScore('sentence-medium')

    def test_getSentenceLengthScore_full_ideal(self):
        self._test_getSentenceLengthScore('sentence-ideal')

    def test_getSentenceLengthScore_over_ideal(self):
        self._test_getSentenceLengthScore('sentence-overlong')

    def _test_getSentencePositionScore(self, pos, sentence_count, expected):
        """Test Parser.getSentencePositionScore

        Arguments:
            pos {int} -- sentence position (0-based)
            sentence_count {int} -- number of sentences (len())
            expected {float} -- expected score
        """
        parser = Parser()
        result = parser.getSentencePositionScore(pos, sentence_count)

        assert_ex(
            'sentence position score',
            result,
            expected,
            hint='/'.join([str(pos), str(sentence_count)]))

    def test_getSentencePositionScore_first(self):
        self._test_getSentencePositionScore(0, 10, .17)

    def test_getSentencePositionScore_second(self):
        self._test_getSentencePositionScore(1, 10, .23)

    def test_getSentencePositionScore_last(self):
        self._test_getSentencePositionScore(9, 10, .15)

    def _test_getTitleScore(self, sample_name):
        """Test Parser.getTitleScore with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        samp = Sample(DATA_PATH, sample_name)
        parser = Parser(lang=samp.d['lang'])
        title = samp.d['compareTitle']
        sentence = samp.d['compareWords']

        expected = samp.d['titleScore']
        result = parser.getTitleScore(title, sentence)

        assert_ex(
            'title score',
            result,
            expected,
            hint=[title, sentence])

    def test_getTitleScore_poor(self):
        self._test_getTitleScore('sentence-1word')

    def test_getTitleScore_short(self):
        self._test_getTitleScore('sentence-short')

    def test_getTitleScore_medium(self):
        self._test_getTitleScore('sentence-medium')

    def test_getTitleScore_ideal(self):
        self._test_getTitleScore('sentence-ideal')

    def test_getTitleScore_overlong(self):
        self._test_getTitleScore('sentence-overlong')

    def _test_splitSentences(self, sample_name):
        """Test Parser.splitSentences with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        samp = Sample(DATA_PATH, sample_name)
        parser = Parser(lang=samp.d['lang'])

        expected = samp.d['splitSentences']
        result = parser.splitSentences(samp.d['text'])

        assert_ex(
            'sentence split',
            result,
            expected)

    def test_splitSentences_single(self):
        self._test_splitSentences('sentence-short')

    def test_splitSentences_multi(self):
        self._test_splitSentences('sentence-list')

    def _test_splitWords(self, sample_name):
        """Test Parser.splitWords with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        samp = Sample(DATA_PATH, sample_name)
        parser = Parser(lang=samp.d['lang'])
        text = samp.d['text']

        expected = samp.d['splitWords']
        result = parser.splitWords(text)

        assert_ex(
            'word split',
            expected,
            result)

    def test_splitWords_empty(self):
        self._test_splitWords('empty')

    def test_splitWords_single(self):
        self._test_splitWords('sentence-1word')

    def test_splitWords_multi(self):
        self._test_splitWords('sentence-medium')

    def _test_removePunctations(self, sample_name):
        """Test Parser.removePunctations with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        samp = Sample(DATA_PATH, sample_name)
        parser = Parser(lang=samp.d['lang'])

        expected = samp.d['removePunctations']
        result = parser.removePunctations(samp.d['text'])

        assert_ex(
            'punctuation removal',
            result,
            expected)

    def test_removePunctations_empty(self):
        self._test_removePunctations('empty')

    def test_removePunctations_single(self):
        self._test_removePunctations('sentence-1word')

    def test_removePunctations_multi(self):
        self._test_removePunctations('sentence-list')

    def _test_removeStopWords(self, sample_name):
        """Test Parser.removeStopWords with data from the selected sample

        Arguments:
            sample_name {str} -- name of data source
        """
        samp = Sample(DATA_PATH, sample_name)
        parser = Parser(lang=samp.d['lang'])
        words = parser.splitWords(samp.d['text'])

        expected = samp.d['removeStopWords']
        result = parser.removeStopWords(words)

        assert_ex(
            'remove stop words',
            result,
            expected)

    def test_removeStopWords_empty(self):
        self._test_removeStopWords('empty')

    def test_removeStopWords_single(self):
        self._test_removeStopWords('sentence-1word')

    def test_removeStopWords_simple(self):
        self._test_removeStopWords('sentence-2words')

    def test_removeStopWords_multi(self):
        self._test_removeStopWords('sentence-list')
