from textteaser.parser import Parser
from .sample import Sample
from .assert_ex import assert_ex


class TestParser:
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
        samp = Sample(sample_name)
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
        parser = Parser()
        samp = Sample(sample_name)
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
        samp = Sample(sample_name)
        parser = Parser()
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
        samp = Sample(sample_name)
        parser = Parser()

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
        samp = Sample(sample_name)
        parser = Parser()
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
        parser = Parser()
        samp = Sample(sample_name)

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
        parser = Parser()
        samp = Sample(sample_name)
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
