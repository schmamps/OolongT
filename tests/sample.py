""" Load sample data """
from oolongt import simple_io
from pathlib import Path


class Sample:
    def __init__(self, root, name):
        base = str(root.joinpath(name))
        data = simple_io.load_json(base + '.json')

        if data['text'] is False:
            data['text'] = self.join_sentences(data['sentences'])

        self.d = data
        self.name = name

    def join_sentences(self, sentence_list):
        """Create text from sentence list

        Arguments:
            sentence_list {List[Dict]} -- loaded sentences

        Returns:
            str -- text
        """
        return '\n  '.join([sent['text'] for sent in sentence_list])

    @property
    def text(self):
        return self.d['text']

    @property
    def title(self):
        return self.d['title']
