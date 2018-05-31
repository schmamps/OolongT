""" Load sample data """
from oolongt import simple_io
from pathlib import Path


class Sample:
    def __init__(self, root, name):
        base = str(root.joinpath(name))
        data = simple_io.load_json(base + '.json')
        keys = [key for key in data.keys() if key != 'meta']

        if data['text'] is False:
            if 'sentences' in keys:
                data['text'] = self.join_sentences(data['sentences'])

            else:
                data['text'] = simple_io.read_file(base + '.txt')

        self.d = data

    def join_sentences(self, sentence_list):
        """Create text from sentence list

        Arguments:
            sentence_list {List[Dict]} -- loaded sentences

        Returns:
            str -- text
        """

        return '\n  '.join([sent['text'] for sent in sentence_list])
