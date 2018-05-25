
    def _test_scoreKeyword(self, keyword, wordCount, expected):
        summ = Summarizer()

        result = summ.scoreKeyword(keyword, wordCount)

        assert result == expected

    def test_scoreKeyword_zero(self):
        keyword = {'count': 0}
        wordCount = 1
        expected = 0

        self._test_scoreKeyword(keyword, wordCount, expected)

    def test_scoreKeyword_third(self):
        keyword = {'count': 1}
        wordCount = 3
        expected = 0.5

        self._test_scoreKeyword(keyword, wordCount, expected)

    def test_scoreKeyword_half(self):
        keyword = {'count': 1}
        wordCount = 2
        expected = 0.75

        self._test_scoreKeyword(keyword, wordCount, expected)

    def test_scoreKeyword_max(self):
        keyword = {'count': 1}
        wordCount = 1
        expected = 1.5

        self._test_scoreKeyword(keyword, wordCount, expected)
