import typing
from collections import OrderedDict
from pathlib import Path


from src.oolongt.parser import Parser
from src.oolongt.typedefs import ScoredKeyword
from setup.generate import generate_set, get_final_path, process_keywords
from setup.util import math
from tests.typedefs import Sample

SAMPLING_SIZE = 10


def dictify(keyword: ScoredKeyword) -> OrderedDict:
    kw_dict = OrderedDict()  # type: OrderedDict[str, typing.Any]
    kw_dict['score'] = keyword.score
    kw_dict['count'] = keyword.count
    kw_dict['word'] = keyword.word

    return kw_dict


def get_median_keywords(samp: Sample) -> typing.List[ScoredKeyword]:
    p = Parser()
    samples = [p.get_keywords(samp.body) for _ in range(SAMPLING_SIZE)]

    mean = samples[0].copy()
    for kw_idx in range(len(mean)):
        mean[kw_idx].score = math.median([s[kw_idx].score for s in samples])

    return mean


def get_output_path(output_path: Path, sample_name: str) -> Path:
    return output_path.joinpath('{}.keywords.json'.format(sample_name))


def get_dict(keyword_count: int, keywords: typing.List[ScoredKeyword]):
    data = OrderedDict()  # type: OrderedDict[str, typing.Any]
    data['keyword_count'] = keyword_count
    data['keywords'] = [dictify(kw) for kw in keywords]

    return data


def process_sample(
        samp: Sample,
        _: Path,
        output_path: Path
        ) -> typing.Tuple[typing.Dict, Path]:
    received = get_median_keywords(samp)
    keywords = sorted(received, reverse=True)
    keyword_count = sum([kw.count for kw in keywords])

    data = get_dict(keyword_count, keywords)
    file_path = get_final_path(output_path, 'keywords', samp.name)

    return data, file_path


def generate(input_path: Path, output_path: Path) -> bool:
    return generate_set(
        'keywords',
        process_sample,
        input_path,
        output_path,
        post_proc=process_keywords)
