from pathlib import Path

from tests import helpers  # circular dependency hack
from tests.typedefs.sample import Sample


def get_sample_paths():
    root = Path(__file__).parent.parent.parent.joinpath('tests', 'data')

    # pylint: disable=no-member
    return root.glob('*.json')


def get_samples():
    root = Path(__file__).parent.parent.parent.joinpath('tests', 'data')

    # pylint: disable=no-member
    for file in get_sample_paths():
        yield Sample(root, file.stem)
