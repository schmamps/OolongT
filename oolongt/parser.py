"""Text parser"""
import typing
from re import sub

import nltk.data
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

from oolongt.typedefs.parser_config import BUILTIN, DEFAULT_LANG, ParserConfig
from oolongt.typedefs.scored_keyword import ScoredKeyword
from oolongt.typedefs.scored_sentence import ScoredSentence


def remove_punctuations(text: str) -> str:
    """Remove non-space, non-alphanumeric characters from `text`

    Arguments:
        text {str} -- ex: 'It\'s 4:00am, you say?'

    Returns:
        str -- ex: 'Its 400am you say'
    """
    unpunct = ''.join(t for t in text if t.isalnum() or t.isspace())

    return unpunct


def split_words(text: str, language: str) -> typing.Iterator[str]:
    """List constituent words of `text` via tokenizer sequentially

    Arguments:
        sentence {str} -- text to split

    Returns:
        typing.List[str] -- words in text
    """
    split = word_tokenize(text.lower(), language=language)

    return split


class Parser:
    def __init__(self, root: str = BUILTIN, lang: str = DEFAULT_LANG) -> None:
        """Initialize class with `root`/`lang`.json

        Keyword Arguments:
            root {str} -- root directory of language data
                (default: {parser.BUILTIN})
            lang {str} -- basename of language file
                (default: {parser.DEFAULT_LANG})

        Raises:
            ValueError: missing/invalid configuration file
        """
        config = ParserConfig(root, lang)
        isl = config.ideal_sentence_length
        language = config.nltk_language
        stop_words = config.stop_words

        self.ideal_sentence_length = isl  # type: int
        self.language = language          # type: str
        self.stop_words = stop_words      # type: typing.List[str]
        self._stemmer = PorterStemmer(mode=PorterStemmer.MARTIN_EXTENSIONS)

    def get_words(
            self,
            text: str,
            stop_words=True,
            stem=False,
            ) -> typing.List[str]:
        bare = remove_punctuations(text).lower()
        words = split_words(bare, self.language)

        if not stop_words:
            words = self.filter_stop_words(words)

        if stem:
            words = self.stem(words)

        return list(words)

    def get_all_words(self, text: str) -> typing.List[str]:
        """List words in `text` sequentially

        Arguments:
            text {str} -- text

        Returns:
            typing.List[str] -- words in text
        """
        return self.get_words(text)

    def get_all_stems(self, text: str) -> typing.List[str]:
        """List all stems in `text` sequentially

        Arguments:
            text {str} -- text

        Returns:
            typing.List[str] -- stems in text
        """
        return self.get_words(text, stem=True)

    def get_key_words(self, text: str) -> typing.List[str]:
        """List all meaningful words in `text`

        Arguments:
            text {str} -- text

        Returns:
            typing.List[str] -- words in text, minus stop words
        """
        return self.get_words(text, stop_words=False)

    def get_key_stems(self, text: str) -> typing.List[str]:
        """List all meaningful stems in `text`

        Arguments:
            text {str} -- text

        Returns:
            typing.List[str] -- words in text, minus stop words
        """
        return self.get_words(text, stop_words=False, stem=True)

    def get_keywords(self, text: str) -> typing.List[ScoredKeyword]:
        """List scored keywords in `text`

        Arguments:
            text {str} -- text

        Returns:
            typing.List[ScoredKeyword] -- list of keywords, scored
        """
        keyword_stems = self.get_key_stems(text)
        unique_stems = list(set(keyword_stems))

        keywords = [
            ScoredKeyword(word, keyword_stems.count(word), len(keyword_stems))
            for word
            in unique_stems]

        return keywords

    def split_sentences(self, text: str) -> typing.List[str]:
        """List sentences in `text` via tokenizer sequentially

        Arguments:
            text {str} -- body of content

        Returns:
            typing.List[str] -- sentences in text
        """
        normalized = sub('\\s+', ' ', text)

        return sent_tokenize(normalized, language=self.language)

    def filter_stop_words(
            self,
            words: typing.Iterator[str]
            ) -> typing.Iterator[str]:
        """Filter `words` not in `self.stop_words`

        Arguments:
            words {typing.Iterator[str]} -- word list

        Returns:
            typing.Iterator[str] -- filter() of words
        """
        return filter(self.is_not_stop_word, words)

    def stem(
            self,
            words: typing.Iterator[str]
            ) -> typing.Iterator[str]:
        """Map words with stemmer

        Arguments:
            words {typing.Iterator[str]} -- word list

        Returns:
            typing.Iterator[str] -- stem list
        """
        return map(self._stemmer.stem, words)

    def is_not_stop_word(self, word: str) -> bool:
        """Verify word is not in self.stop_words

        Arguments:
            word {str} -- word

        Returns:
            bool -- word not in stop words
        """
        return word not in self.stop_words
