""" Load sample data """
from oolongt import simple_io, nodash
from pathlib import Path


class Sample:
    def __init__(self, root, name):
        # type: (str, str) -> None
        base = str(root.joinpath(name))
        data = simple_io.load_json(base + '.json')

        if data['text'] is False:
            data['text'] = self.join_sentences(data['sentences'])

        self.d = data
        self.name = name

    def join_sentences(self, sentence_list):
        # type: (list[dict]) -> str
        """Create text from sentence list

        Arguments:
            sentence_list {list[dict]} -- loaded sentences

        Returns:
            str -- text
        """
        return '\n  '.join(nodash.pluck(sentence_list, 'text'))

    @property
    def text(self):
        # type: () -> str
        return self.d['text']

    @property
    def title(self):
        # type: () -> str
        return self.d['title']
