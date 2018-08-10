"""Text summarizer"""
import typing

from oolongt.constants import BUILTIN, DEFAULT_IDIOM, TOP_KEYWORD_MIN_RANK
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
        kws: typing.Sequence[ScoredKeyword]
        ) -> float:
    """Get minimum frequency for top `kws`

    Arguments:
        keywords {typing.List[ScoredKeyword]} -- list of scored keywords

    Returns:
        int -- minimum frequency
    """
    if (len(kws) == 0):
        return 0

    limit = TOP_KEYWORD_MIN_RANK
    minimum = sorted(
        kws, reverse=True)[:limit].pop()  # type: ScoredKeyword

    return minimum.score


def score_by_dbs(
        sentence_words: typing.List[str],
        top_kws: typing.Sequence[ScoredKeyword],
        top_kw_words: typing.List[str]
        ) -> float:
    """Score sentence (`sentence_word_list`) by keyword density

    Arguments:
        sentence_words {typing.List[str]} --
            sequential list of words in sentence
        top_kws {typing.List[dict]} --
            top keywords in content body
        top_kw_words {typing.List[str]} --
            values of 'word' in top_keywords

    Returns:
        float  -- density based score
    """
    k = len(list(set(sentence_words) & set(top_kw_words))) + 1
    summ = 0.0
    first_word = {}   # type: typing.Dict[str, float]
    second_word = {}  # type: typing.Dict[str, float]

    for i, word in enumerate(sentence_words):
        if word in top_kw_words:
            index = top_kw_words.index(word)

            if first_word == {}:
                first_word = {
                    'i': i,
                    'score': top_kws[index].score}
            else:
                second_word = first_word
                first_word = {
                    'i': i,
                    'score': top_kws[index].score}
                distance = first_word['i'] - second_word['i']

                summ += (first_word['score'] * second_word['score']) / (distance ** 2)  # nopep8

    dbs = (1.0 / k * (k + 1.0)) * summ

    return dbs


def score_by_sbs(
        sentence_words: typing.List[str],
        top_kws: typing.Sequence[ScoredKeyword],
        top_kw_words: typing.List[str]
        ) -> float:
    """Score sentence (`words`) by summation

    Arguments:
        sentence_words {typing.List[str]} --
            sequential list of words in sentence
        top_kws {typing.Sequence[ScoredKeyword]} -- top keywords in body
        top_kw_words {typing.List[str]} -- values of 'word' in top_keywords

    Returns:
        float -- score
    """
    summ = 0.0

    if len(sentence_words) == summ:
        return summ

    for word in [x for x in sentence_words if x in top_kw_words]:
        index = top_kw_words.index(word)
        score = top_kws[index].score

        summ += score

    sbs = 1.0 / len(sentence_words) * summ

    return sbs


class Summarizer:
    def __init__(
            self,
            root: str = BUILTIN,
            idiom: str = DEFAULT_IDIOM
            ) -> None:
        self.parser = Parser(root, idiom)

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
        title_kw_words = self.parser.get_key_words(title)
        top_kws = self.get_top_keywords(body, source, category)
        top_kw_stems = pluck_keyword_words(top_kws)
        of = len(sentences)

        scored_sentences = [
            self.get_sentence(
                text, idx, of,
                title_kw_words, top_kws, top_kw_stems)
            for idx, text in enumerate(sentences)]

        return scored_sentences

    def get_top_keywords(
            self,
            body: str,
            source: typing.Any,
            category: typing.Any
            ) -> typing.List[ScoredKeyword]:
        """List 1st-10th ranked keywords in `text`

        Arguments:
            body {str} -- body of content
            source {any} -- unused
            category {any} -- unused

        Returns:
            list[ScoredKeyword] -- most frequent keywords
        """
        keywords = self.parser.get_keywords(body)
        minimum = get_top_keyword_threshold(keywords)
        top_kws = [kw for kw in keywords if kw.score >= minimum]

        return top_kws

    def get_sentence(
            self,
            text: str,
            index: int,
            of: int,
            title_kw_words: typing.List[str],
            top_kws: typing.Sequence[ScoredKeyword],
            top_kw_stems: typing.List[str]
            ) -> ScoredSentence:
        """Score sentence (`text`) on several factors

        Arguments:
            text {str} -- text of sentence
            index {int} -- index of sentence in overall text (zero based)
            of {int} -- len() of sentences in `text`
            title_kw_words {typing.List[str]} -- key words in title
            top_kws {typing.List[ScoredKeyword]} -- top keywords in body
            top_kw_stems {typing.List[str]} -- values of 'word' in top_keywords

        Returns:
            ScoredSentence -- scored sentence
        """
        sentence_stems = self.parser.get_all_stems(text)

        title_score = self.score_by_title(title_kw_words, sentence_stems)
        length_score = self.score_by_length(sentence_stems)
        dbs_score = score_by_dbs(
            sentence_stems, top_kws, top_kw_stems)
        sbs_score = score_by_sbs(
            sentence_stems, top_kws, top_kw_stems)

        scored = ScoredSentence(
                text, index, of,
                title_score, length_score, dbs_score, sbs_score)

        return scored

    def score_by_length(self, sentence_words: typing.List[str]) -> float:
        """Score sentence by its count of `sentence_word_list` vs. ideal

        Arguments:
            sentence_words {typing.List[str]} --
                list of words in the sentence

        Returns:
            float -- score
        """
        ideal = float(self.parser.ideal_sentence_length)
        score = ideal - abs(ideal - len(sentence_words))
        score /= ideal

        return score

    def score_by_title(
            self,
            title_kw_words: typing.List[str],
            sentence_words: typing.List[str]
            ) -> float:
        """Score `sentence_word_list` by matches with `title_words`

        Arguments:
            title_kw_words {typing.List[str]} -- key words in title
            sentence_words {typing.List[str]} --
                list of words in the sentence

        Returns:
            float -- score
        """
        matched_kw_words = [
            word
            for word in sentence_words
            if word in title_kw_words]

        score = _float_len(matched_kw_words) / _float_len(title_kw_words)

        return score
