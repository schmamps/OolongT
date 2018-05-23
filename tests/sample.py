""" Load sample data """
import json
import os.path as path
from typing import Dict, Tuple, List


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

    def load_json(self, path: str) -> Dict:
        contents = self.read_file(path)

        return json.loads(contents)

    def read_file(self, path: str) -> str:
        with open(path, 'r', encoding='utf-8') as file:
            contents = file.read()

        return contents

    def join_sentences(self, sentence_list: List[Dict]) -> str:
        return '\n  '.join([sent['text'] for sent in sentence_list])
