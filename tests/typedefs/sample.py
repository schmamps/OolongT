"""Load sample data"""
import typing
from pathlib import Path

from src.oolongt import simple_io
from tests.typedefs.sample_keyword import SampleKeyword
from tests.typedefs.sample_sentence import SampleSentence


def join_sentences(
        sentence_list: typing.List[typing.Dict[str, typing.Any]]
        ) -> str:
    """Create text from sentence list

    Arguments:
        sentence_list {typing.List[typing.Dict[str, typing.Any]]} --
            loaded sentences

    Returns:
        str -- text
    """
    return '\n  '.join([sent['text'] for sent in sentence_list])


def load_config(root: Path, name: str) -> typing.Dict[str, typing.Any]:
    """Load initialization data for Sample

    Arguments:
        root {str} -- root directory of idiom config
        idiom {str} -- basename of idiom config

    Returns:
        typing.Dict[str, typing.Any] -- initialization data
    """
    path = root.joinpath(name + '.json')
    config = simple_io.load_json(path)

    text = config.pop('text', False)
    sentences = config.pop('sentences', [{'text': ''}])
    sent_of = len(sentences)
    keywords = config.pop('keywords', [])
    kw_of = config.get('keyword_count', 0)

    config['body'] = text or join_sentences(sentences)
    config['sentences'] = [
        SampleSentence(data_dict, sent_of) for data_dict in sentences]
    config['keywords'] = [
        SampleKeyword(data_dict, kw_of) for data_dict in keywords]

    return config


class Sample(object):
    def __init__(self, root: Path, name: str) -> None:
        config = load_config(root, name)
        config.update({'name': name})

        self._data = config
        self._keys = config.keys()

    def __getattr__(self, name: str) -> typing.Any:
        if name in self._keys:
            return self._data[name]

        raise AttributeError('Property {!r} not found'.format(name))
