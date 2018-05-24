""" Load sample data """
import json
import os.path as path
from sys import version_info
from io import open as io_open


class Sample:
    def __init__(self, name):
        base = '/'.join([path.dirname(__file__), 'data', name + '.'])
        data = self.load_json(base + 'json')
        keys = [key for key in data.keys() if key != 'meta']

        if data['text'] is False:
            if 'sentences' in keys:
                data['text'] = self.join_sentences(data['sentences'])

            else:
                data['text'] = self.read_file(base + 'txt')

        self.d = {}

        for key in keys:
            self.d[key] = data[key]

    def load_json(self, path):
        """Load data from the specified path

        Arguments:
            path {str} -- path to file

        Returns:
            Dict -- data in file
        """
        contents = self.read_file(path)

        return json.loads(contents)

    def read_file(self, path):
        """Load text from the specified path

        Arguments:
            path {str} -- path to file

        Returns:
            str -- text in file
        """

        contents = ''

        with io_open(path, 'r', encoding='utf-8') as file:
            contents = file.read()

        if version_info < (3, 0):
            contents = contents.encode('ascii', 'ignore')

        return contents

    def join_sentences(self, sentence_list):
        """Create text from sentence list

        Arguments:
            sentence_list {List[Dict]} -- loaded sentences

        Returns:
            str -- text
        """

        return '\n  '.join([sent['text'] for sent in sentence_list])
