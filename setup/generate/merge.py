import typing
from collections import OrderedDict
from pathlib import Path

from setup.generate import generate_set, get_final_path, process_keywords
from setup.util import json_data
from src.oolongt.parser import ScoredKeyword
from tests.typedefs import Sample


PROJECT_ROOT = Path(__file__).parent.parent.parent


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


def get_sentences(original, generated) -> typing.List[ScoredKeyword]:
    sentence_count = len(generated)
    if len(original) != sentence_count:
        raise ValueError('sentence count mismatch')

    sentences = [
        get_sentence(generated[index], original[index])
        for index in range(sentence_count)]

    return sentences


def get_dict(
        samp: Sample,
        original: OrderedDict,
        keywords: OrderedDict,
        sentences: OrderedDict
        ) -> OrderedDict:
    data = OrderedDict()  # type: OrderedDict[str, typing.Any]
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

    return data


def process_sample(
        samp: Sample,
        input_path: Path,
        output_path: Path
        ) -> typing.Tuple[typing.Dict, Path]:
    original = json_data.read(
        input_path.joinpath(samp.name + '.json'))
    keywords = json_data.read(
        get_final_path(output_path, 'keywords', samp.name))
    sentences = json_data.read(
        get_final_path(output_path, 'sentences', samp.name))

    data = get_dict(samp, original, keywords, sentences)
    file_path = get_final_path(output_path, 'merge', samp.name)

    return data, file_path


def generate(input_path: Path, output_path: Path) -> bool:
    return generate_set(
        'merge',
        process_sample,
        input_path,
        output_path,
        post_proc=process_keywords)
