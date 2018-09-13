"""Merge original and generated sample data"""
import typing
from collections import OrderedDict
from pathlib import Path

from setup.generate import generate_set, get_final_path, process_keywords
from setup.util import json_data
from tests.typings import Sample

PROJECT_ROOT = Path(__file__).parent.parent.parent


def get_sentence(
        original: OrderedDict,
        generated: OrderedDict) -> OrderedDict:
    """Merge original with generated

    Arguments:
        original {OrderedDict} -- original sentence data
        generated {OrderedDict} -- generated sentence data

    Returns:
        OrderedDict -- merged sentence data
    """
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
    sentence = OrderedDict()  # type: OrderedDict[str, typing.Any]
    for key in keys:
        sentence[key] = generated[key]

    return sentence


def get_sentences(
        original: OrderedDict,
        generated: OrderedDict) -> typing.List[OrderedDict]:
    """Merge non-generated data with generated

    Arguments:
        original {OrderedDict} -- non-generated data
        generated {OrderedDict} -- generated data

    Raises:
        ValueError -- wrong sentence count

    Returns:
        typing.List[OrderedDict] -- merged sentences
    """
    sentence_count = len(generated)
    if len(original) != sentence_count:
        raise ValueError('sentence count mismatch')

    sentences = [
        get_sentence(original[index], generated[index])
        for index in range(sentence_count)]

    return sentences


def get_dict(
        samp: Sample,
        original: OrderedDict,
        keywords: OrderedDict,
        sentences: OrderedDict) -> OrderedDict:
    """Get OrderedDict with merged data

    Arguments:
        samp {Sample} -- sample
        original {OrderedDict} -- original sample
        keywords {OrderedDict} -- sample keywords
        sentences {OrderedDict} -- sample sentences

    Returns:
        OrderedDict -- sample data
    """
    data = OrderedDict()  # type: OrderedDict[str, typing.Any]
    for key in original.keys():
        key_value = original[key]

        if key in ['keyword_count', 'keywords']:
            data[key] = keywords[key]

        elif key == 'sentences':
            if samp.sentences:
                data[key] = get_sentences(
                    original[key], sentences[key])

        else:
            data[key] = key_value

    return data


def process_sample(
        samp: Sample,
        input_path: Path,
        output_path: Path) -> typing.Tuple[typing.Dict, Path]:
    """Process `samp` for output

    Arguments:
        samp {Sample} -- sample data
        _ {Path} -- ignored
        output_path {Path} -- output directory

    Returns:
        typing.Tuple[typing.Dict, Path] -- sample data, output path
    """
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
    """Merge generated data from `input_path` to `output_path`

    Arguments:
        input_path {Path} -- path to input files
        output_path {Path} -- path to output files

    Returns:
        bool -- success
    """

    return generate_set(
        'merge',
        process_sample,
        input_path,
        output_path,
        post_proc=process_keywords)
