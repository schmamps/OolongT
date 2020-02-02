"""Load sample data"""
import typing
from pathlib import Path

from src.oolongt.io import load_json
from src.oolongt.typings import DictOfAny
from tests.typings.sample_keyword import SampleKeyword
from tests.typings.sample_sentence import SampleSentence
from tests.typings.typings import SampleKeywordList, SampleSentenceList


def join_sentences(sentence_list: typing.List[DictOfAny]) -> str:
    """Create text from sentence list

    Arguments:
        sentence_list {typing.List[typing.Dict[str, typing.Any]]} --
            loaded sentences

    Returns:
        str -- text
    """
    return '\n  '.join([sent['text'] for sent in sentence_list])


def load_config(root: Path, name: str) -> DictOfAny:
    """Load initialization data for Sample

    Arguments:
        root {str} -- root directory of idiom config
        idiom {str} -- basename of idiom config

    Returns:
        DictOfAny -- initialization data
    """
    path = root.joinpath(name + '.json')
    config = load_json(path)

    text = config.pop('text', False)
    sentences = config.pop('sentences', [{'text': ''}])
    sent_of = len(sentences)
    keywords = config.pop('keywords', [])
    kw_of = sum([kw['count'] for kw in keywords])

    config['body'] = text or join_sentences(sentences)
    config['sentences'] = [
        SampleSentence(data_dict, sent_of) for data_dict in sentences]
    config['keywords'] = [
        SampleKeyword(data_dict, kw_of) for data_dict in keywords]

    return config


class Sample:
    """Sample content"""
    def __init__(self, root: Path, name: str) -> None:
        """Initialize Sample

        Arguments:
            root {Path} -- path to idioms
            name {str} -- name of idiom
        """
        config = load_config(root, name)
        config.update({'name': name})

        self._data = config
        self._keys = config.keys()

    @property
    def title(self) -> str:
        return self._data['title']['text']

    @property
    def title_keywords(self) -> str:
        return self._data['title']['filtered']

    @property
    def body(self) -> str:
        """Get body

        Returns:
            str -- full text of sample
        """
        return self._data['body']

    @property
    def keywords(self) -> SampleKeywordList:
        """List keywords

        Returns:
            SampleKeywordList - sample keywords
        """
        return self._data['keywords']

    @property
    def sentences(self) -> SampleSentenceList:
        """List sentences

        Returns:
            SampleSentenceList -- sample sentences
        """
        return self._data['sentences']

    def __getattr__(self, name: str) -> typing.Any:
        """Get miscellaneous attributes

        Arguments:
            name {str} -- attribute name

        Raises:
            AttributeError -- attribute does not exist

        Returns:
            typing.Any -- value of attribute
        """
        if name in self._keys:
            return self._data[name]

        raise AttributeError('Property {!r} not found'.format(name))
