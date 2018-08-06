from io import open as io_open
from math import floor
from pytest import approx
from time import time

from generator.util import json, console

from oolongt.summarizer import Summarizer

from tests.constants import DATA_PATH, SAMPLES
from tests.helpers import (
    assert_ex, get_samples, randomize_list, snip)
from tests.typing.sample import Sample

from nltk.corpus import stopwords


def print_list(desc, items):
    fmt = '{{0:{0}d}}. {{1}}'.format(len(str(len(items))))

    print(desc.upper())
    print('-' * len(desc))

    for i, item in enumerate(items):
        print(fmt.format(i + 1, item))


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


def compare_lists():
    summ = Summarizer()
    nltk_words = sorted(list(set([
        summ.parser.remove_punctuations(w)
        for w in stopwords.words(summ.parser.language)])))
    user_words = sorted(list(set(
        json.read('./.champs/en-old.json')['stop_words']['user'])))

    console.group('NLTK Uniques')
    console.ul(sorted([w for w in nltk_words if w not in user_words]))
    console.group_end()

    console.group('User Uniques')
    console.ul(sorted([w for w in user_words if w not in nltk_words]))
    console.group_end()


compare_lists()
