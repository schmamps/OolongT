from collections import OrderedDict
from json import load
from pathlib import Path
from re import match

from generator.util import console, get_samples, json as json_util, math
from oolongt.simple_io import load_json


PROJECT_ROOT = Path(__file__).parent.parent.parent


def join_path(subs, *file_comps):
    file_name = '.'.join(list(file_comps) + ['json'])

    return PROJECT_ROOT.joinpath(subs).joinpath(file_name)


def get_sample_path(samp):
    return join_path('tests/data', samp.name)


def get_generated_path(samp, key):
    return join_path('generator/output', samp.name, key)


def get_sentence(generated, original):
    generated['id'] = original.get('id')
    keys = filter(
        lambda x: generated.get(x) is not None,
        [
            'index',
            'id',
            'sbs_score',
            'dbs_score',
            'title_score',
            'length_score',
            'position_score',
            'keyword_score',
            'total_score',
            'text',
            'rank',
        ])

    sentence = OrderedDict()
    for key in keys:
        sentence[key] = generated[key]

    return sentence


def get_sentences(original, generated):
    sentence_count = len(generated)
    if len(original) != sentence_count:
        raise ValueError('sentence count mismatch')

    sentences = [
        get_sentence(generated[index], original[index])
        for index in range(sentence_count)]

    return sentences


def generate():
    console.group('Merging')
    for samp in get_samples():
        console.group(samp.name)

        file_comps = [samp.name]
        file_path = json_util.get_output_path(file_comps, 'merged.json')

        try:
            original = json_util.read(
                get_sample_path(samp))
            keywords = json_util.read(
                get_generated_path(samp, 'keywords'))
            sentences = json_util.read(
                get_generated_path(samp, 'sentences'))

            data = OrderedDict()

            for key in original.keys():
                key_value = original[key]

                if key in ['keyword_count', 'keywords']:
                    data[key] = keywords[key]

                elif key == 'sentences':
                    if (len(samp.sentences) > 0):
                        data[key] = get_sentences(
                            original[key], sentences[key])

                else:
                    data[key] = key_value

            json_util.write(file_path, data, kludge='keywords')

            console.success('saved to: {}'.format(file_path))

        except Exception as e:
            console.error(e)
            console.info('deleting: {!r}'.format(file_path))

            json_util.cleanup(file_comps)

        console.group_end()

    console.group_end()
