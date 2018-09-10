import typing
from collections import OrderedDict
from pathlib import Path

from setup.generate import generate_set, get_final_path
from setup.util import math
from src.oolongt.summarizer import ScoredSentence, Summarizer
from tests.typedefs import Sample

SAMPLING_SIZE = 25


def dictify(received, rank):
    sent_dict = OrderedDict()
    sent_dict['index'] = received.index
    sent_dict['sbs_score'] = received.sbs_score
    sent_dict['dbs_score'] = received.dbs_score
    sent_dict['title_score'] = received.title_score
    sent_dict['length_score'] = received.length_score
    sent_dict['position_score'] = received.position_score
    sent_dict['keyword_score'] = received.keyword_score
    sent_dict['total_score'] = received.total_score
    sent_dict['text'] = received.text
    sent_dict['rank'] = rank

    return sent_dict


def get_median_sentence(all_samples, sent_idx):
    samples = [s[sent_idx] for s in all_samples]

    sbs_score = math.median([s.sbs_score for s in samples])
    dbs_score = math.median([s.dbs_score for s in samples])
    title_score = math.median([s.title_score for s in samples])
    length_score = math.median([s.length_score for s in samples])
    keyword_score = math.median([s.keyword_score for s in samples])
    total_score = math.median([s.total_score for s in samples])

    samples[0].sbs_score = sbs_score
    samples[0].dbs_score = dbs_score
    samples[0].title_score = title_score
    samples[0].length_score = length_score
    samples[0].keyword_score = keyword_score
    samples[0].total_score = total_score

    return samples[0]


def get_median_sentences(samp: Sample):
    summ = Summarizer()
    all_samples = [
        summ.get_all_sentences(samp.body, samp.title, None, None)
        for _ in range(SAMPLING_SIZE)]

    mean = all_samples[0].copy()
    for sent_idx in range(len(mean)):
        mean[sent_idx] = get_median_sentence(all_samples, sent_idx)

    return mean


def get_output_path(output_path: Path, sample_name: str) -> Path:
    return output_path.joinpath('{}.keywords.json'.format(sample_name))


def get_dict(
        ranks: typing.List[int],
        receiveds: typing.List[ScoredSentence]
        ) -> OrderedDict:
    data = OrderedDict()  # type: OrderedDict
    data['sentences'] = [
        dictify(sent, ranks.index(idx))
        for idx, sent in enumerate(receiveds)]

    return data


def process_sample(
        samp: Sample,
        _: Path,
        output_path: Path
        ) -> typing.Tuple[typing.Dict, Path]:
    receiveds = get_median_sentences(samp)
    ranks = [sent.index for sent in sorted(receiveds, reverse=True)]

    data = get_dict(ranks, receiveds)
    file_path = get_final_path(output_path, 'sentences', samp.name)

    return data, file_path


def generate(input_path: Path, output_path: Path) -> bool:
    return generate_set('sentences', process_sample, input_path, output_path)
