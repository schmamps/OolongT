"""keyword data generator"""
import typing
from collections import OrderedDict
from pathlib import Path

from setup.generate import generate_set, get_final_path, process_keywords
from setup.util import math
from src.oolongt.parser import Parser, ScoredKeyword
from tests.typings import Sample

SAMPLING_SIZE = 10


def dictify(keyword: ScoredKeyword) -> OrderedDict:
    """Cast ScoredKeyword `keyword` to OrderedDict

    Arguments:
        keyword {ScoredKeyword} -- scored keyword

    Returns:
        OrderedDict -- keyword as dict
    """
    kw_dict = OrderedDict()  # type: OrderedDict[str, typing.Any]
    kw_dict['score'] = keyword.score
    kw_dict['count'] = keyword.count
    kw_dict['word'] = keyword.word

    return kw_dict


# pylint: disable=consider-using-enumerate
def get_median_keywords(samp: Sample) -> typing.List[ScoredKeyword]:
    """Get median keyword scores

    Arguments:
        samp {Sample} -- sample data

    Returns:
        typing.List[ScoredKeyword] -- ScoredKeyword with median score
    """
    parser = Parser()
    samples = [parser.get_keywords(samp.body) for _ in range(SAMPLING_SIZE)]

    median = samples[0].copy()
    for kw_idx, _ in enumerate(median):
        median[kw_idx].score = math.median([s[kw_idx].score for s in samples])

    return median


# pylint: enable=consider-using-enumerate
def get_dict(
        keyword_count:
        int, keywords: typing.List[ScoredKeyword]) -> OrderedDict:
    """Get keyword data as dictionary

    Arguments:
        keyword_count {int} -- number of keywords (non-unique)
        keywords {typing.List[ScoredKeyword]} -- scored keywords

    Returns:
        OrderedDict -- keyword data
    """
    data = OrderedDict()  # type: OrderedDict[str, typing.Any]
    data['keyword_count'] = keyword_count
    data['keywords'] = [dictify(kw) for kw in keywords]

    return data


def process_sample(
        samp: Sample,
        _: Path,
        output_path: Path) -> typing.Tuple[dict, Path]:
    """Process `samp` for output

    Arguments:
        samp {Sample} -- sample data
        _ {Path} -- ignored
        output_path {Path} -- output directory

    Returns:
        typing.Tuple[dict, Path] -- sample data, output path
    """
    received = get_median_keywords(samp)
    keywords = sorted(received, reverse=True)
    keyword_count = sum([kw.count for kw in keywords])

    data = get_dict(keyword_count, keywords)
    file_path = get_final_path(output_path, 'keywords', samp.name)

    return data, file_path


def generate(input_path: Path, output_path: Path) -> bool:
    """Generate keyword data from `input_path` to `output_path`

    Arguments:
        input_path {Path} -- path to input files
        output_path {Path} -- path to output files

    Returns:
        bool -- success
    """
    return generate_set(
        'keywords',
        process_sample,
        input_path,
        output_path,
        post_proc=process_keywords)
