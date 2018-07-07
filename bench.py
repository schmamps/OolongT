from io import open as io_open
from math import floor
from pytest import approx
from time import time

from oolongt.nodash import pluck, sort_by
from oolongt.summarizer import Summarizer

from tests.constants import DATA_PATH, SAMPLES
from tests.helpers import (
    assert_ex, compare_dict, get_samples, randomize_list, snip)
from tests.typing.sample import Sample


def report(title, *data):
    results = [{'desc': x[0], 'time': x[1]} for x in data]
    pad = max([len(x['desc']) for x in results])
    formatter = '{{0:{0}s}}: {{1:.6f}}s'.format(pad)
    by_speed = sorted(results, key=lambda x: x['time'])

    lines = [title.upper(), '=']
    for result in by_speed:
        lines += [formatter.format(result['desc'], result['time'])]

    for num, line in enumerate(lines):
        text = line
        if num == 1:
            text *= max([len(x) for x in lines])

        print(text)

    print(
        '\ndifference: {0:.3f}x'.format(
            by_speed[-1]['time'] / by_speed[0]['time']))
    print('')
