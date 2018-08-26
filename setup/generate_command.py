"""Generate Data"""
import typing  # noqa
from pathlib import Path
from setuptools import Command

from setup.generate import keywords, merge, sentences  # noqa


class GenerateCommand(Command):
    user_options = []  # type: typing.List[tuple]

    """Generate test data"""
    def initialize_options(self):
        root = Path(__file__).parent.parent
        self.input_dir = root.joinpath('tests', 'data', 'text')
        self.output_dir = root.joinpath('generated_data')

    def finalize_options(self):
        pass

    def run(self):
        self.announce('generating test data', level=2)
        for module in [keywords, sentences, merge]:
            module.generate(self.input_dir, self.output_dir)
