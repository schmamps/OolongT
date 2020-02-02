"""Text parser"""
import typing
from re import sub

from nltk.stem.porter import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

from ..typings import StringList
from .parser_config import BUILTIN, DEFAULT_IDIOM, ParserConfig
from .scored_keyword import ScoredKeyword


def remove_punctuations(text: str) -> str:
    """Remove non-space, non-alphanumeric characters from `text`

    Arguments:
        text {str} -- ex: 'It\'s 4:00am, you say?'

    Returns:
        str -- ex: 'Its 400am you say'
    """
    unpunct = ''.join(t for t in text if t.isalnum() or t.isspace())

    return unpunct


class Parser:
    """Parse content for words and keywords"""
    def __init__(
            self,
            root: str = BUILTIN,
            idiom: str = DEFAULT_IDIOM) -> None:
        """Initialize class with `root`/`idiom`.json

        Keyword Arguments:
            root {str} -- root directory of idiom data
                (default: {parser.BUILTIN})
            idiom {str} -- basename of idiom file
                (default: {parser.DEFAULT_IDIOM})

        Raises:
            ValueError: missing/invalid configuration file
        """
        config = ParserConfig(root, idiom)
        isl = config.ideal_sentence_length
        language = config.language
        stop_words = config.stop_words

        self.ideal_sentence_length = isl  # type: int
        self.language = language          # type: str
        self.stop_words = stop_words      # type: StringList
        self._stemmer = PorterStemmer(mode=PorterStemmer.MARTIN_EXTENSIONS)

    def get_words(
            self,
            text: str,
            keep_stop_words=True,
            stem=False) -> StringList:
        """List of words from `text`

        Arguments:
            text {str} -- text

        Keyword Arguments:
            keep_stop_words {bool} -- keep stop words (default: {True})
            stem {bool} -- get word stems instead of whole (default: {False})

        Returns:
            StringList -- list of words
        """
        words = self.split_words(text)

        if not keep_stop_words:
            words = filter(self.is_not_stop_word, words)

        if stem:
            words = map(self._stemmer.stem, words)

        return list(words)

    def get_all_words(self, text: str) -> StringList:
        """List words in `text` sequentially

        Arguments:
            text {str} -- text

        Returns:
            StringList -- words in text
        """
        return self.get_words(text)

    def get_all_stems(self, text: str) -> StringList:
        """List all stems in `text` sequentially

        Arguments:
            text {str} -- text

        Returns:
            StringList -- stems in text
        """
        return self.get_words(text, stem=True)

    def get_key_words(self, text: str) -> StringList:
        """List all meaningful words in `text`

        Arguments:
            text {str} -- text

        Returns:
            StringList -- words in text, minus stop words
        """
        return self.get_words(text, keep_stop_words=False)

    def get_key_stems(self, text: str) -> StringList:
        """List all meaningful stems in `text`

        Arguments:
            text {str} -- text

        Returns:
            StringList -- words in text, minus stop words
        """
        return self.get_words(text, keep_stop_words=False, stem=True)

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

    def split_sentences(self, text: str) -> StringList:
        """List sentences in `text` via tokenizer sequentially

        Arguments:
            text {str} -- body of content

        Returns:
            StringList -- sentences in text
        """
        normalized = sub('\\s+', ' ', text)

        return sent_tokenize(normalized, language=self.language)

    def split_words(self, text: str) -> typing.Iterator[str]:
        """List constituent words of `text` via tokenizer sequentially

        Arguments:
            sentence {str} -- text to split

        Returns:
            StringList -- words in text
        """
        bare = remove_punctuations(text).lower()
        split = word_tokenize(bare.lower(), language=self.language)

        return split

    def is_not_stop_word(self, word: str) -> bool:
        """Verify word is not in self.stop_words

        Arguments:
            word {str} -- word

        Returns:
            bool -- word not in stop words
        """
        return word not in self.stop_words
