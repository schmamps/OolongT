""" Load sample data """
from oolongt import simple_io, nodash
from pathlib import Path


def join_sentences(sentence_list):
    # type: (list[dict]) -> str
    """Create text from sentence list

    Arguments:
        sentence_list {list[dict]} -- loaded sentences

    Returns:
        str -- text
    """
    return '\n  '.join(nodash.pluck(sentence_list, 'text'))


class Sample:
    def __init__(self, root, name):
        # type: (str, str) -> None
        base = str(root.joinpath(name))
        data = simple_io.load_json(base + '.json')

        data['name'] = name
        if data['text'] is False:
            data['text'] = join_sentences(data['sentences'])

        self._data = data
        self._keys = data.keys()

    def __getattr__(self, name):
        if name in self._keys:
            return self._data[name]

        raise AttributeError('Property {0!r} not found'.format(name))
