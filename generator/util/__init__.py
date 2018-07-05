from pathlib import Path

from tests import helpers  # circular dependency hack
from tests.typing.sample import Sample


def get_samples():
    root = Path(__file__).parent.parent.parent.joinpath('tests', 'data')

    # pylint: disable=no-member
    for file in root.glob('*.json'):
        stem = file.stem

        print(stem.upper())
        print('=' * len(stem))

        yield Sample(root, file.stem)
