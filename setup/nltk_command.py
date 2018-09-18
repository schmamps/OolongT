"""Download NLTK Data"""
import sys
import typing  # noqa  pylint: disable=unused-import

import nltk
from setuptools import Command


def download():
    """Start NLTK downloader"""
    print('start download')
    nltk.download()
    print('end download')


class NltkCommand(Command):
    """NLTK download command"""
    user_options = []  # type: typing.List[tuple]

    def initialize_options(self):
        """dummy"""
        pass

    def finalize_options(self):
        """dummy"""
        pass

    def box(self, msg):
        """Announce presence of downloader window"""
        cap = '{{}}{}{{}}'.format('\u2550' * (len(msg) + 2))

        self.announce(cap.format('\u2554', '\u2557'), level=2)
        self.announce('\u2551 {} \u2551'.format(msg), level=2)
        self.announce(cap.format('\u255A', '\u255D'), level=2)

    def run(self):
        """Run NLTK download command"""
        self.box(
            'Opening the NLTK downloader... look for a new desktop window')
        sys.stdout.write('\a')

        download()
