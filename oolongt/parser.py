"""Text parser"""
import typing
from re import sub

import nltk.data
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


def split_words(text: str, language: str) -> typing.List[str]:
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

    def get_all_words(self, text: str) -> typing.List[str]:
        """List words in `text` sequentially

        Arguments:
            text {str} -- text

        Returns:
            typing.List[str] -- words in text
        """
        bare = remove_punctuations(text)
        split = split_words(bare, self.language)

        return split

    def get_keyword_strings(self, text: str) -> typing.List[str]:
        """List all meaningful words in `text`

        Arguments:
            text {str} -- text

        Returns:
            typing.List[str] -- words in text, minus stop words
        """
        all_strings = self.get_all_words(text)
        keyword_strings = self.remove_stop_words(all_strings)

        return keyword_strings

    def get_keywords(self, text: str) -> typing.List[ScoredKeyword]:
        """List scored keywords in `text`

        Arguments:
            text {str} -- text

        Returns:
            typing.List[ScoredKeyword] -- list of keywords, scored
        """
        all_kw_strs = self.get_keyword_strings(text)
        unique_kw_strs = list(set(all_kw_strs))

        scored_kws = [
            ScoredKeyword(word, all_kw_strs.count(word), len(all_kw_strs))
            for word
            in unique_kw_strs]

        return scored_kws

    def split_sentences(self, text: str) -> typing.List[str]:
        """List sentences in `text` via tokenizer sequentially

        Arguments:
            text {str} -- body of content

        Returns:
            typing.List[str] -- sentences in text
        """
        normalized = sub('\\s+', ' ', text)

        return sent_tokenize(normalized, language=self.language)

    def remove_stop_words(self, words: typing.List[str]) -> typing.List[str]:
        """Filter stop words from `words`

        Arguments:
            words {typing.List[str]} -- all words in text

        Returns:
            typing.List[str] -- words not matching a stop word
        """
        filtered = [word for word in words if word not in self.stop_words]

        return filtered
