"""Text summarizer"""
import typing

from oolongt.constants import BUILTIN, DEFAULT_LANG, TOP_KEYWORD_MIN_RANK
from oolongt.parser import Parser
from oolongt.typedefs.scored_keyword import ScoredKeyword
from oolongt.typedefs.scored_sentence import ScoredSentence


def pluck_keyword_words(
        keyword_list: typing.Sequence[ScoredKeyword]
        ) -> typing.List[str]:
    """List every word property in `keyword_list`

    Arguments:
        keyword_list {typing.List[ScoredKeyword]} -- list of scored keywords

    Returns:
        typing.List[str] -- all words in keyword list
    """
    return [kw.word for kw in keyword_list]


def _float_len(val_list: typing.Sized) -> float:
    """Cast length of sized value as a float

    Arguments:
        val_list {typing.List[typing.Any]} -- list of items

    Returns:
        float -- length of list as float
    """
    return float(len(val_list))


def get_top_keyword_threshold(
        keywords: typing.Sequence[ScoredKeyword]
        ) -> float:
    """Get minimum frequency for top `keywords`

    Arguments:
        keywords {list[ScoredKeyword]} -- list of scored keywords

    Returns:
        int -- minimum frequency
    """
    if (len(keywords) == 0):
        return 0

    limit = TOP_KEYWORD_MIN_RANK
    minimum = sorted(
        keywords, reverse=True)[:limit].pop()  # type: ScoredKeyword

    return minimum.score


def score_by_dbs(
        sentence_word_list: typing.List[str],
        top_keywords: typing.Sequence[ScoredKeyword],
        top_keyword_list: typing.List[str]
        ) -> float:
    """Score sentence (`sentence_word_list`) by keyword density

    Arguments:
        sentence_word_list {typing.List[str]} --
            sequential list of words in sentence
        top_keywords {typing.List[dict]} --
            top keywords in content body
        top_keyword_list {typing.List[str]} --
            values of 'word' in top_keywords

    Returns:
        float  -- density based score
    """
    k = len(list(set(sentence_word_list) & set(top_keyword_list))) + 1
    summ = 0.0
    first_word = {}   # type: typing.Dict[str, float]
    second_word = {}  # type: typing.Dict[str, float]

    for i, word in enumerate(sentence_word_list):
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


def score_by_sbs(
        words: typing.List[str],
        top_keywords: typing.Sequence[ScoredKeyword],
        top_keyword_list: typing.List[str]
        ) -> float:
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


class Summarizer:
    def __init__(self, root: str = BUILTIN, lang: str = DEFAULT_LANG) -> None:
        self.parser = Parser(root, lang)

    def get_all_sentences(
            self,
            body: str,
            title: str,
            source=None,
            category=None
            ) -> typing.List[ScoredSentence]:
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
            self.get_sentence(
                text, idx, of,
                title_words, top_keywords, top_keyword_list)
            for idx, text in enumerate(sentences)]

        return scored_sentences

    def get_top_keywords(
            self,
            text: str,
            source: typing.Any,
            category: typing.Any
            ) -> typing.List[ScoredKeyword]:
        """List 1st-10th ranked keywords in `text`

        Arguments:
            text {str} -- body of content
            source {any} -- unused
            category {any} -- unused

        Returns:
            list[ScoredKeyword] -- most frequent keywords
        """
        keywords = self.parser.get_keywords(text)
        minimum = get_top_keyword_threshold(keywords)
        top_keywords = [kw for kw in keywords if kw.score >= minimum]

        return top_keywords

    def get_sentence(
            self,
            text: str,
            index: int,
            of: int,
            title_words: typing.List[str],
            top_keywords: typing.Sequence[ScoredKeyword],
            top_keyword_list: typing.List[str]
            ) -> ScoredSentence:
        """Score sentence (`text`) on several factors

        Arguments:
            text {str} -- text of sentence
            index {int} -- index of sentence in overall text (zero based)
            of {int} -- len() of sentences in `text`
            title_words {list[str]} -- words in title
            top_keywords {list[ScoredKeyword]} -- top keywords in content body
            top_keyword_list {list[str]} -- values of 'word' in top_keywords

        Returns:
            ScoredSentence -- scored sentence
        """
        sentence_word_list = self.parser.get_all_words(text)

        title_score = self.score_by_title(title_words, sentence_word_list)
        length_score = self.score_by_length(sentence_word_list)
        dbs_score = score_by_dbs(
            sentence_word_list, top_keywords, top_keyword_list)
        sbs_score = score_by_sbs(
            sentence_word_list, top_keywords, top_keyword_list)

        scored = ScoredSentence(
                text, index, of,
                title_score, length_score, dbs_score, sbs_score)

        return scored

    def score_by_length(self, sentence_word_list: typing.List[str]) -> float:
        """Score sentence by its count of `sentence_word_list` vs. ideal

        Arguments:
            sentence_word_list {typing.List[str]} --
                list of words in the sentence

        Returns:
            float -- score
        """
        ideal = float(self.parser.ideal_sentence_length)
        score = ideal - abs(ideal - len(sentence_word_list))
        score /= ideal

        return score

    def score_by_title(
            self,
            title_words: typing.List[str],
            sentence_word_list: typing.List[str]
            ) -> float:
        """Score `sentence_word_list` by matches with `title_words`

        Arguments:
            title {str} -- title of the text content
            text {str} -- body of content

        Returns:
            float -- score
        """
        sentence_keywords = self.parser.remove_stop_words(sentence_word_list)
        matched_keywords = [
            word
            for word in sentence_keywords
            if word in title_words]

        score = _float_len(matched_keywords) / _float_len(title_words)

        return score
