"""Text summarizer"""
from . import parser
from .typing.scored_sentence import ScoredSentence


def pluck_keyword_words(keyword_list):
    # type: (list[dict]) -> list[str]
    return [kw.word for kw in keyword_list]


class Summarizer:
    def __init__(self, root=parser.BUILTIN, lang=parser.DEFAULT_LANG):
        # type: (str, str) -> None
        self.parser = parser.Parser(root, lang)

    def get_sentences(self, body, title, source, category):
        # type: (str, str, any, any) -> list[ScoredSentence]
        """List and score all sentences in `text`

        Arguments:
            body {str} -- body of content
            title {str} -- title of content
            source {any} -- unused
            category {any} -- unused

        Returns:
            list[ScoredSentence] -- list of scored sentences
        """
        sentences = self.parser.split_sentences(body)
        title_words = self.parser.get_keyword_strings(title)
        top_keywords = self.get_top_keywords(body, source, category)
        top_keyword_list = pluck_keyword_words(top_keywords)
        of = len(sentences)

        scored_sentences = [
            self.get_scored_sentence(
                text, idx, of,
                title_words, top_keywords, top_keyword_list)
            for idx, text in enumerate(sentences)]

        return scored_sentences

    def get_top_keyword_threshold(self, keywords):
        # type: (list[ScoredKeyword]) -> int
        """Get minimum frequency for top `keywords`

        Arguments:
            keywords {list[ScoredKeyword]} -- list of scored keywords

        Returns:
            int -- minimum frequency
        """
        if (len(keywords) == 0):
            return 0

        tenth = sorted(
            keywords, reverse=True)[:10].pop()  # type: ScoredKeyword

        return tenth.score

    def get_top_keywords(self, text, source, category):
        # type: (str, any, any) -> list[dict]
        """List 1st-10th ranked keywords in `text`

        Arguments:
            text {str} -- body of content
            source {any} -- unused
            category {any} -- unused

        Returns:
            list[ScoredKeyword] -- most frequent keywords
        """
        keywords = self.parser.get_keywords(text)
        minimum = self.get_top_keyword_threshold(keywords)
        top_keywords = [kw for kw in keywords if kw.score >= minimum]

        return top_keywords

    def get_scored_sentence(self, text, index, of,
                            title_words, top_keywords, top_keyword_list):
        # type: (str, int, int, list, list, list[str], int) -> ScoredSentence
        """Score sentence (`text`) on several factors

        Arguments:
            idx {int} -- zero-based position of sentence in overall text
            text {str} -- text of sentence
            title_words {list[str]} -- words in title
            top_keywords {list[dict]} -- top keywords in content body
            top_keyword_list {list[str]} -- values of 'word' in top_keywords
            num_sents {int} -- number of sentences in overall text

        Returns:
            dict -- {total_score: float, sentence: str, index: int}
        """
        words = self.parser.get_all_words(text)

        title_score = self.score_title(title_words, words)
        length_score = self.score_sentence_length(words)
        dbs_score = self.score_dbs(words, top_keywords, top_keyword_list)
        sbs_score = self.score_sbs(words, top_keywords, top_keyword_list)

        scored = ScoredSentence(
                text, index, of,
                title_score, length_score, dbs_score, sbs_score)

        return scored

    def score_dbs(self, words, top_keywords, top_keyword_list):
        # type: (list[str], list[ScoredKeyword], list[str]) -> float
        """Score sentence (`words`) by keyword density

        Arguments:
            words {list[str]} -- sequential list of words in sentence
            top_keywords {list[dict]} -- top keywords in content body
            top_keyword_list {list[str]} -- values of 'word' in top_keywords

        Returns:
            float  -- density based score
        """
        k = len(list(set(words) & set(top_keyword_list))) + 1
        summ = 0.0
        first_word = {}
        second_word = {}

        for i, word in enumerate(words):
            if word in top_keyword_list:
                index = top_keyword_list.index(word)

                if first_word == {}:
                    first_word = {
                        'i': i,
                        'score': top_keywords[index].score}
                else:
                    second_word = first_word
                    first_word = {
                        'i': i,
                        'score': top_keywords[index].score}
                    distance = first_word['i'] - second_word['i']

                    summ += (first_word['score'] * second_word['score']) / (distance ** 2)  # nopep8

        dbs = (1.0 / k * (k + 1.0)) * summ

        return dbs

    def score_sbs(self, words, top_keywords, top_keyword_list):
        # type: (list[str], list[ScoredKeyword], list[str]) -> float
        """Score sentence (`words`) by summation

        Arguments:
            words {list[str]} -- sequential list of words in sentence
            top_keywords {list[dict]} -- top keywords in content body
            top_keyword_list {list[str]} -- values of 'word' in top_keywords

        Returns:
            float -- score
        """
        summ = 0.0

        if len(words) == summ:
            return summ

        for word in [x for x in words if x in top_keyword_list]:
            index = top_keyword_list.index(word)
            score = top_keywords[index].score

            summ += score

        sbs = 1.0 / len(words) * summ

        return sbs

    def score_sentence_length(self, words):
        # type: list[str] -> float
        """Score sentence (`words`) based on actual word count vs. ideal

        Arguments:
            words {list[str]} -- list of words in the sentence

        Returns:
            float -- score
        """
        ideal = float(self.parser.ideal_sentence_length)
        score = ideal - abs(ideal - len(words))
        score /= ideal

        return score

    def score_title(self, title_words, sentence_words):
        # type: (list[str], list[str]) -> float
        """Score `sentence_words` by matches with `title_words`

        Arguments:
            title {str} -- title of the text content
            text {str} -- body of content

        Returns:
            float -- score
        """
        title_keywords = self.parser.remove_stop_words(title_words)
        sentence_keywords = self.parser.remove_stop_words(sentence_words)
        matched_keywords = [
            word
            for word in sentence_keywords
            if word in title_keywords]

        score = float(len(matched_keywords)) / (len(title_keywords) * 1.0)

        return score
