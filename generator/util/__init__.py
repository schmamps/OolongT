from pathlib import Path

from tests.sample import Sample


def get_samples():
    root = Path(__file__).parent.parent.parent.joinpath('tests', 'data')

    # pylint: disable=no-member
    for file in root.glob('*.json'):
        stem = file.stem

        print(stem.upper())
        print('=' * len(stem))

        yield Sample(root, file.stem)
