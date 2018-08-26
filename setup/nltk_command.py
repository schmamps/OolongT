"""Download NLTK Data"""
import typing  # noqa
import sys
from setuptools import Command

import nltk


def download():
    print('start download')
    nltk.download()
    print('end download')


class NltkCommand(Command):
    user_options = []  # type: typing.List[tuple]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def box(self, msg):
        cap = '{{}}{}{{}}'.format('\u2550' * (len(msg) + 2))

        self.announce(cap.format('\u2554', '\u2557'), level=2)
        self.announce('\u2551 {} \u2551'.format(msg), level=2)
        self.announce(cap.format('\u255A', '\u255D'), level=2)

    def run(self):
        self.box(
            'Opening the NLTK downloader... look for a new desktop window')
        sys.stdout.write('\a')

        download()
