from io import open as io_open
from math import floor

from oolongt.nodash import pluck, sort_by
from oolongt.summarizer import Summarizer

from tests.constants import DATA_PATH, SAMPLES
from tests.helpers import (
    assert_ex, compare_float, compare_dict, get_samples, randomize_list, snip)
from tests.sample import Sample


def create_json(major, minor):
    return io_open(
        './' + '.'.join([major, minor, 'json']), 'w', encoding='utf8')


def open_json(key, wrap):
    opened = '{{\n\t"{0}": '.format(key)

    if wrap:
        opened += wrap + '\n'

    return opened


def close_json(wrap):
    closed = '\n}'

    if wrap:
        closed = '\n\t{0}'.format(wrap) + closed

    return closed


def jsonify_property(obj, prop, fmt='s'):
    val = obj[prop]
    if isinstance(val, str):
        val = '"{0}"'.format(val)

    formatter = '\t\t\t"{{0}}": {{1:{0}}}'.format(fmt)
    formatted = formatter.format(prop, val)

    return formatted


def jsonify_sentence(sent):
    pairs = ',\n'.join([
        jsonify_property(sent, 'order', 'd'),
        jsonify_property(sent, 'sbs', '.8f'),
        jsonify_property(sent, 'dbs', '.8f'),
        jsonify_property(sent, 'title_score', '.8f'),
        jsonify_property(sent, 'length_score', '.8f'),
        jsonify_property(sent, 'position_score', '.2f'),
        jsonify_property(sent, 'keyword_score', '.8f'),
        jsonify_property(sent, 'total_score', '.8f'),
        jsonify_property(sent, 'text'),
        jsonify_property(sent, 'rank', 'd'),
    ])

    return '\t\t{\n' + pairs + '\n\t\t}'


def generate_sentences():
    for samp in get_samples(*SAMPLES):
        summ = Summarizer()

        receiveds = summ.get_sentences(
            samp.d['text'], samp.d['title'], None, None)

        by_score = sorted(receiveds, key=lambda x: -x['total_score'])
        for rank, _ in enumerate(by_score):
            by_score[rank]['rank'] = rank

        by_order = sorted(by_score, key=lambda x: x['order'])

        with create_json(samp.name, 'sent') as file:
            file.write(open_json('sentences', '['))

            file.write(',\n'.join(
                [jsonify_sentence(x) for x in by_order]
            ))

            file.write(close_json(']'))


generate_sentences()
