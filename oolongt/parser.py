# !/usr/bin/python
# -*- coding: utf-8 -*-
from json import JSONDecodeError
from pathlib import Path

import nltk.data

from .simple_io import load_json

BUILTIN = Path(__file__).parent.joinpath('lang')
DEFAULT_LANG = 'en'
JSON_SUFFIX = '.lang.json'
TOKEN_SUFFIX = '.tokenizer.pickle'


class Parser:
    def __init__(self, path=BUILTIN, lang=DEFAULT_LANG):
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
        cfg_data = self.load_language(path, lang)

        try:
            self.language = cfg_data['meta']['name']
            self.ideal = int(cfg_data['ideal'])
            self.stop_words = cfg_data['stop_words']
            self.token_path = cfg_data['token_path']

        except (JSONDecodeError, KeyError):
            raise ValueError(
                'Invalid configuration for ' + lang + ' in ' + path)

    def load_language(self, path, lang):
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
        root = Path(path)
        sub = root.joinpath(lang)

        try:
            # pylint: disable=no-member
            sub.resolve().relative_to(root.resolve())

        except ValueError:
            raise PermissionError('directory traversal in lang: ' + lang)

        json_path = sub.joinpath(lang + JSON_SUFFIX)
        token_path = sub.joinpath(lang + TOKEN_SUFFIX)

        # pylint: disable=no-member
        if not json_path.exists() or not token_path.exists():
            raise FileNotFoundError('config dir: ' + str(root))

        cfg_data = load_json(str(json_path))
        cfg_data['token_path'] = str(token_path)

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
            text {str} -- any text

        Returns:
            List[str] -- words in text, minus stop words
        """
        all_words = self.get_all_words(text)
        keywords = self.remove_stop_words(all_words)

        return keywords

    def count_keyword(self, unique_word, all_words):
        """Count number of instances of unique_word in all_words

        Arguments:
            unique_word {str} -- word
            all_words {List[str]} -- list of all words in text

        Returns:
            Dict -- {word: unique_word, count: (instances in all_words)}
        """
        return {
            'word': unique_word,
            'count': all_words.count(unique_word)}

    def get_keywords(self, text):
        """Get counted list of keywords and total number of keywords

        Arguments:
            text {str} -- text

        Returns:
            Tuple[List[Dict], int] -- individual and total keyword counts
        """
        all_words = self.get_keyword_list(text)
        keywords = [
            self.count_keyword(unique_word, all_words)
            for unique_word
            in list(set(all_words))]

        return (keywords, len(all_words))

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
        normalized = (index + 1) / (sentence_count * 1.0)

        if normalized > 0 and normalized <= 0.1:
            return 0.17
        elif normalized > 0.1 and normalized <= 0.2:
            return 0.23
        elif normalized > 0.2 and normalized <= 0.3:
            return 0.14
        elif normalized > 0.3 and normalized <= 0.4:
            return 0.08
        elif normalized > 0.4 and normalized <= 0.5:
            return 0.05
        elif normalized > 0.5 and normalized <= 0.6:
            return 0.04
        elif normalized > 0.6 and normalized <= 0.7:
            return 0.06
        elif normalized > 0.7 and normalized <= 0.8:
            return 0.04
        elif normalized > 0.8 and normalized <= 0.9:
            return 0.04
        elif normalized > 0.9 and normalized <= 1.0:
            return 0.15
        else:
            raise ValueError(' '.join([
                'Invalid index:',
                str(index),
                'where sentence count:',
                str(sentence_count)]))

    def get_title_score(self, title, text):
        """Score text by keywords in title

        Arguments:
            title {str} -- title of the text content
            text {str} -- text content

        Returns:
            float -- score
        """
        title_words = self.remove_stop_words(title)
        sentence_words = self.remove_stop_words(text)
        matched_words = [
            word
            for word in sentence_words
            if word in title_words]

        score = len(matched_words) / (len(title) * 1.0)

        return score

    def split_sentences(self, text):
        """Split sentences via tokenizer

        Arguments:
            text {str} -- text to split by sentence

        Returns:
            List[str] -- sequential list of sentences in text
        """
        tokenizer = nltk.data.load('file:' + self.token_path, format='pickle')

        return tokenizer.tokenize(text)

    def split_words(self, text):
        """Split text into sequential list of constituent words

        Arguments:
            sentence {str} -- text to split

        Returns:
            List[str] -- list of words in text
        """
        split = text.lower().split()

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
        filtered = [word for word in words if word not in self.stop_words]

        return filtered
