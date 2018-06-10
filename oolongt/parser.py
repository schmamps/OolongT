# !/usr/bin/python
# -*- coding: utf-8 -*-
from json import JSONDecodeError
from math import ceil
from pathlib import Path
from re import sub

import nltk.data
from nltk.tokenize import sent_tokenize, word_tokenize

from .simple_io import load_json

BUILTIN = Path(__file__).parent.joinpath('lang')
DEFAULT_LANG = 'en'
JSON_SUFFIX = '.json'


class Parser:
    def __init__(self, root=BUILTIN, lang=DEFAULT_LANG):
        """Initialize class for specified language

        Load data from:
            {path}/{lang}/{lang}.lang.json
            {path}/{lang}/{lang}.tokenizer.pickle

        Keyword Arguments:
            path {any} -- override builtin language dir
            lang {str} -- subdir of path containing data (default: {'en'})

        Raises:
            PermissionError: directory traversal in lang
            FileNotFoundError: language files  not found
            ValueError: incomplete/malformed configuration file
        """
        cfg_data = self.load_language(root, lang)

        try:
            self.language = cfg_data['nltk_language']
            self.ideal = int(cfg_data['ideal'])
            self.stop_words = cfg_data['stop_words']

        except (JSONDecodeError, KeyError):
            raise ValueError(
                'Invalid configuration for ' + lang + ' in ' + root)

    def load_language(self, root, lang):
        """Load language from specified path

        Arguments:
            path {str} -- Root directory for language data
            lang {str} -- subdirectory for specific language

        Raises:
            PermissionError -- Directory traversal via lang
            FileNotFoundError -- Language file(s) not found

        Returns:
            Dict -- data in language JSON + path to tokenizer pickle
        """
        root_path = Path(root)
        cfg_path = root_path.joinpath(lang + '.json')
        cfg_path_str = str(cfg_path)

        try:
            # pylint: disable=no-member
            cfg_path.resolve().relative_to(root_path.resolve())

        except ValueError:
            raise PermissionError('directory traversal in lang: ' + lang)

        # pylint: disable=no-member
        if not cfg_path.exists():
            raise FileNotFoundError('config: ' + cfg_path_str)

        cfg_data = load_json(cfg_path_str)

        return cfg_data

    def get_all_words(self, text):
        """Get all the words from a text

        Arguments:
            text {str} -- text

        Returns:
            List[str] -- sequential list of words in text
        """
        bare = self.remove_punctuations(text)
        split = self.split_words(bare)

        return split

    def get_keyword_list(self, text):
        """Extract all meaningful words from text into a list

        Arguments:
            text {str} -- text

        Returns:
            List[str] -- words in text, minus stop words
        """
        all_words = self.get_all_words(text)
        keywords = self.remove_stop_words(all_words)

        return keywords

    def count_keyword(self, word, all_words):
        """Count number of instances of unique_word in all_words

        Arguments:
            unique_word {str} -- word
            all_words {List[str]} -- list of all words in text

        Returns:
            Dict -- {word: unique_word, count: (instances in all_words)}
        """
        return {
            'word': word,
            'count': all_words.count(word)}

    def get_keywords(self, text):
        """Get counted list of keywords and total number of keywords

        Arguments:
            text {str} -- text

        Returns:
            Tuple[List[Dict], int] -- individual and total keyword counts
        """
        all_keywords = self.get_keyword_list(text)
        unique_words = list(set(all_keywords))

        counted_keywords = [
            self.count_keyword(word, all_keywords)
            for word
            in unique_words]

        return (counted_keywords, len(all_keywords))

    def get_sentence_length_score(self, words):
        """Score sentence based on actual word count vs. ideal

        Arguments:
            words {List[str]} -- list of words in the sentence

        Returns:
            float -- score
        """
        score = (self.ideal - abs(self.ideal - len(words))) / self.ideal

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
        title_keywords = self.remove_stop_words(title_words)
        sentence_keywords = self.remove_stop_words(sentence_words)
        matched_keywords = [
            word
            for word in sentence_keywords
            if word in title_keywords]

        score = len(matched_keywords) / (len(title_keywords) * 1.0)

        return score

    def split_sentences(self, text):
        """Split sentences via tokenizer

        Arguments:
            text {str} -- body of content

        Returns:
            List[str] -- sequential list of sentences in text
        """
        normalized = sub('\\s+', ' ', text)

        return sent_tokenize(normalized, language=self.language)

    def split_words(self, text):
        """Split text into sequential list of constituent words

        Arguments:
            sentence {str} -- text to split

        Returns:
            List[str] -- list of words in text
        """
        split = word_tokenize(text.lower())

        return split

    def remove_punctuations(self, text):
        """Remove non-space, non-alphanumeric characters from string

        Arguments:
            text {str} -- ex: 'It\'s 4:00am, you say?'

        Returns:
            str -- ex: 'Its 400am you say'
        """
        unpunct = ''.join(t for t in text if t.isalnum() or t.isspace())

        return unpunct

    def remove_stop_words(self, words):
        """Get sequential list of non-stopwords in supplied list of words

        Arguments:
            words {List[str]} -- all words in text

        Returns:
            List[str] -- words not matching a stop word
        """
        filtered = [word for word in words if word not in self.stop_words]

        return filtered
