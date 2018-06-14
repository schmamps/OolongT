#!/usr/bin/python
# -*- coding: utf-8 -*-
from math import ceil

from . import parser
from .nodash import pluck, sort_by


class Summarizer:
    def __init__(self, root=parser.BUILTIN, lang=parser.DEFAULT_LANG):
        self.parser = parser.Parser(root, lang)

    def _pluck_words(self, keyword_list):
        return list(pluck(keyword_list, 'word'))

    def get_sentences(self, text, title, source, category):
        """Get list of all sentences in text, sorted by score

        Arguments:
            text {str} -- body of content
            title {str} -- title of content
            source {any} -- unused
            category {any} -- unused

        Returns:
            List[Dict] -- list of sentence Dict(s)
        """
        sentences = self.parser.split_sentences(text)
        title_words = self.parser.get_keyword_list(title)
        top_keywords = self.get_top_keywords(text, source, category)
        top_keyword_list = self._pluck_words(top_keywords)
        num_sents = len(sentences)

        summaries = [
            self.score_sentence(
                idx, sentence,
                title_words, top_keywords, top_keyword_list, num_sents)
            for idx, sentence in enumerate(sentences)]

        return summaries

    def score_keyword(self, keyword, wordCount):
        """Calculate total_score of keyword

        Arguments:
            keyword {Dict} -- {word, count}
            wordCount {int} -- total number of keywords

        Returns:
            Dict -- {word, count, total_score}
        """
        keyword['total_score'] = 1.5 * keyword['count'] / wordCount

        return keyword

    def get_top_keyword_threshold(self, keywords):
        """Get minimum frequency for top keywords

        Arguments:
            keywords {List[Dict]} -- list of keyword Dicts

        Returns:
            int -- minimum frequency
        """
        counts = pluck(keywords, 'count')
        top_10 = sorted(counts, reverse=True)[:10]

        try:
            return top_10.pop()

        except IndexError:
            return 0

    def get_top_keywords(self, text, source, category):
        """Get list of the 1st-10th ranked keywords

        Arguments:
            text {str} -- body of content
            source {any} -- unused
            category {any} -- unused

        Returns:
            List[Dict] -- ten most frequently used words (more if same count)
        """
        keywords, word_count = self.parser.get_keywords(text)
        minimum = self.get_top_keyword_threshold(keywords)
        top_kws = [
            self.score_keyword(kw, word_count)
            for kw in keywords
            if kw['count'] >= minimum]

        return top_kws

    def score_frequency(self, words, top_keywords, keyword_list):
        k = 5.0
        sbs_feature = self.sbs(words, top_keywords, keyword_list)
        dbs_feature = self.dbs(words, top_keywords, keyword_list)
        keyword_freq = k * (sbs_feature + dbs_feature)

        return keyword_freq, sbs_feature, dbs_feature

    def score_sentence(self, idx, text,
                       title_words, top_keywords, top_keyword_list, num_sents):
        """Assign total score to a sentence based on various factors

        Arguments:
            idx {int} -- zero-based position of sentence in overall text
            text {str} -- text of sentence
            title_words {List[str]} -- words in title
            top_keywords {List[Dict]} -- top keywords in overall text
            keyword_list {List[str]} -- values of 'word' in top_keywords
            num_sents {int} -- number of sentences in overall text

        Returns:
            Dict -- {total_score, sentence, order}
        """
        words = self.parser.get_all_words(text)

        title_score = self.get_title_score(title_words, words)
        keyword_score, sbs, dbs = self.score_frequency(
            words, top_keywords, top_keyword_list)
        length_score = self.get_sentence_length_score(words)
        position_score = self.get_sentence_position_score(
            idx, num_sents)

        total_score = (
            title_score * 1.5 +
            keyword_score * 2.0 +
            length_score * 0.5 +
            position_score * 1.0) / 4.0

        return {
            'sbs': sbs,
            'dbs': dbs,
            'title_score': title_score,
            'length_score': length_score,
            'position_score': position_score,
            'keyword_score': keyword_score,
            'total_score': total_score,
            'text': text,
            'order': idx}

    def sbs(self, words, top_keywords, top_keyword_list):
        """Score sentence by keyword score

        Arguments:
            words {List[str]} -- sequential list of words in sentence
            top_keywords {List[Dict]} -- top keywords in overall text
            top_keyword_list {List[str]} -- values of 'word' in top_keywords

        Returns:
            float -- score
        """
        summ = 0.0

        if len(words) == summ:
            return summ

        for word in [x for x in words if x in top_keyword_list]:
            index = top_keyword_list.index(word)
            score = top_keywords[index]['total_score']

            summ += score

        sbs = 1.0 / len(words) * summ

        return sbs

    def dbs(self, words, top_keywords, top_keyword_list):
        """Score sentence by keyword density

        Arguments:
            words {List[str]} -- sequential list of words in sentence
            top_keywords {List[Dict]} -- top keywords in overall text
            top_keyword_list {List[str]} -- values of 'word' in top_keywords

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
                        'score': top_keywords[index]['total_score']}
                else:
                    second_word = first_word
                    first_word = {
                        'i': i,
                        'score': top_keywords[index]['total_score']}
                    distance = first_word['i'] - second_word['i']

                    summ += (first_word['score'] * second_word['score']) / (distance ** 2)  # nopep8

        dbs = (1.0 / k * (k + 1.0)) * summ

        return dbs

    def get_sentence_length_score(self, words):
        """Score sentence based on actual word count vs. ideal

        Arguments:
            words {List[str]} -- list of words in the sentence

        Returns:
            float -- score
        """
        ideal = self.parser.ideal_sentence_length
        score = ideal - abs(ideal - len(words))
        score /= ideal

        return score

    # Jagadeesh, J., Pingali, P., & Varma, V. (2005).
    # Sentence Extraction Based Single Document Summarization.
    # International Institute of Information Technology, Hyderabad, India, 5.
    def get_sentence_position_score(self, index, sentence_count):
        """Score sentence based on position in a list of sentences

        Arguments:
            index {int} -- index of sentence in list
            sentence_count {int} -- length of sentence list

        Returns:
            float -- score
        """
        scores = [.17, .23, .14, .08, .05, .04, .06, .04, .04, .15]

        try:
            score_index = ceil(float(index + 1) / sentence_count * 10) - 1
            position_score = scores[score_index]

            return position_score

        except (IndexError, ZeroDivisionError):
            raise ValueError(' '.join([
                'Invalid index/sentence count: ',
                str(index),
                'of',
                str(sentence_count)]))

    def get_title_score(self, title_words, sentence_words):
        """Score text by keywords in title

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

        score = len(matched_keywords) / (len(title_keywords) * 1.0)

        return score
