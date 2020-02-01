"""sentence data generator"""
import typing
from collections import OrderedDict
from pathlib import Path

from src.oolongt.summarizer import ScoredSentence, Summarizer
from tests.typings import Sample

from ..generate import generate_set, get_final_path
from ..util import math

SAMPLING_SIZE = 25


def dictify(received: ScoredSentence, rank: int) -> OrderedDict:
    """Convert `ScoredSentence` to dict (consistent order)

    Arguments:
        received {ScoredSentence} -- scored sentence
        rank {int} -- rank of sentence

    Returns:
        OrderedDict -- dict of ScoredSentence properies
    """
    sent_dict = OrderedDict()  # type: OrderedDict[str, typing.Any]
    sent_dict['index'] = received.index
    sent_dict['sbs_score'] = received.score.title
    sent_dict['dbs_score'] = received.score.dbs
    sent_dict['title_score'] = received.score.title
    sent_dict['length_score'] = received.score.length
    sent_dict['position_score'] = received.score.position
    sent_dict['keyword_score'] = received.score.keyword
    sent_dict['total_score'] = received.score.total
    sent_dict['text'] = received.text
    sent_dict['rank'] = rank

    return sent_dict


def get_median_sentence(
        all_samples: typing.List[ScoredSentence],
        sent_idx: int) -> ScoredSentence:
    """Get median scores of specific sentence

    Arguments:
        all_samples {typing.List[ScoredSentence]} -- every result
        sent_idx {int} -- index of sentence to average

    Returns:
        ScoredSentence -- median of each score
    """
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


# pylint: disable=consider-using-enumerate
def get_median_sentences(samp: Sample) -> typing.List[ScoredSentence]:
    """Get median sentence scores

    Arguments:
        samp {Sample} -- sample

    Returns:
        typing.List[ScoredSentence] -- scored sentences
    """
    summ = Summarizer()
    all_samples = [
        summ.get_all_sentences(samp.body, samp.title)
        for _ in range(SAMPLING_SIZE)]

    median = all_samples[0].copy()
    for sent_idx, _ in enumerate(median):
        median[sent_idx] = get_median_sentence(all_samples, sent_idx)

    return median


# pylint: enable=consider-using-enumerate
def get_dict(
        ranks: typing.List[int],
        receiveds: typing.List[ScoredSentence]) -> OrderedDict:
    """Get OrderedDict with sentence data

    Arguments:
        ranks {typing.List[int]} -- sentence rankings
        receiveds {typing.List[ScoredSentence]} -- list of sentences

    Returns:
        OrderedDict -- sentence data
    """
    data = OrderedDict()  # type: OrderedDict[str, typing.Any]
    data['sentences'] = [
        dictify(sent, ranks.index(idx))
        for idx, sent in enumerate(receiveds)]

    return data


def process_sample(
        samp: Sample,
        _: Path,
        output_path: Path) -> typing.Tuple[typing.Dict, Path]:
    """Process `samp` for output

    Arguments:
        samp {Sample} -- sample data
        _ {Path} -- ignored
        output_path {Path} -- output directory

    Returns:
        typing.Tuple[typing.Dict, Path] -- sample data, output path
    """
    receiveds = get_median_sentences(samp)
    ranks = [sent.index for sent in sorted(receiveds, reverse=True)]

    data = get_dict(ranks, receiveds)
    file_path = get_final_path(output_path, 'sentences', samp.name)

    return data, file_path


def generate(input_path: Path, output_path: Path) -> bool:
    """Generate sentence data from `input_path` to `output_path`

    Arguments:
        input_path {Path} -- path to input files
        output_path {Path} -- path to output files

    Returns:
        bool -- success
    """
    return generate_set('sentences', process_sample, input_path, output_path)
