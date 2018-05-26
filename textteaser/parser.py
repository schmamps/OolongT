# !/usr/bin/python
# -*- coding: utf-8 -*-
from .simple_io import load_json
from json import JSONDecodeError
import nltk.data
from pathlib import Path, PurePath


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
            self.stopWords = cfg_data['stop_words']
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
        bare = self.removePunctations(text)
        split = self.splitWords(bare)

        return split

    def get_keyword_list(self, text):
        """Extract all meaningful words from text into a list

        Arguments:
            text {str} -- any text

        Returns:
            List[str] -- words in text, minus stop words
        """
        all_words = self.get_all_words(text)
        keywords = self.removeStopWords(all_words)

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

    def getKeywords(self, text):
        all_words = self.get_keyword_list(text)
        keywords = [
            self.count_keyword(unique_word, all_words)
            for unique_word
            in list(set(all_words))]

        return (keywords, len(all_words))

    def getSentenceLengthScore(self, sentence):
        return (self.ideal - abs(self.ideal - len(sentence))) / self.ideal

    # nopep8 Jagadeesh, J., Pingali, P., & Varma, V. (2005). Sentence Extraction Based Single Document Summarization. International Institute of Information Technology, Hyderabad, India, 5.
    def getSentencePositionScore(self, i, sentenceCount):
        normalized = (i + 1) / (sentenceCount * 1.0)

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
            return 0

    def getTitleScore(self, title, sentence):
        titleWords = self.removeStopWords(title)
        sentenceWords = self.removeStopWords(sentence)
        matchedWords = [word for word in sentenceWords if word in titleWords]

        return len(matchedWords) / (len(title) * 1.0)

    def splitSentences(self, text):
        tokenizer = nltk.data.load('file:' + self.token_path, format='pickle')

        return tokenizer.tokenize(text)

    def splitWords(self, sentence):
        return sentence.lower().split()

    def removePunctations(self, text):
        """Remove non-space, non-alphanumeric characters from string

        Arguments:
            text {str} -- ex: 'It\'s 4:00am, you say?'

        Returns:
            str -- ex: 'Its 400am you say'
        """
        return ''.join(t for t in text if t.isalnum() or t.isspace())

    def removeStopWords(self, words):
        return [word for word in words if word not in self.stopWords]
