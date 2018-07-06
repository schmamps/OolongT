""" Load sample data """
from pathlib import Path

from oolongt import nodash, simple_io
from tests.typing.sample_keyword import SampleKeyword
from tests.typing.sample_sentence import SampleSentence


def join_sentences(sentence_list):
    # type: (list[dict]) -> str
    """Create text from sentence list

    Arguments:
        sentence_list {list[dict]} -- loaded sentences

    Returns:
        str -- text
    """
    return '\n  '.join(nodash.pluck(sentence_list, 'text'))


def load_config(root, name):
    path = str(root.joinpath(name + '.json'))
    config = simple_io.load_json(path)

    text = config.pop('text', False)
    sentences = config.pop('sentences', [])
    keywords = config.pop('keywords', [])
    of = len(sentences)

    config['body'] = text if text is not False else join_sentences(sentences)
    config['sentences'] = [
        SampleSentence(data_dict, of) for data_dict in sentences]
    config['keywords'] = [
        SampleKeyword(data_dict) for data_dict in keywords]

    return config


class Sample(object):
    def __init__(self, root, name):
        # type: (str, str) -> None
        config = load_config(root, name)
        config.update({'name': name})

        self._data = config
        self._keys = config.keys()

    def __getattr__(self, name):
        if name in self._keys:
            return self._data[name]

        raise AttributeError('Property {0!r} not found'.format(name))
