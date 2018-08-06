from collections import OrderedDict

from oolongt.summarizer import Summarizer
from oolongt.parser import Parser

from generator.util import console, get_samples, json as json_util, math


SAMPLING_SIZE = 10


def dictify(keyword):
    kw_dict = OrderedDict()
    kw_dict['score'] = keyword.score
    kw_dict['count'] = keyword.count
    kw_dict['word'] = keyword.word

    return kw_dict


def get_mean_keywords(samp):
    p = Parser()
    samples = [p.get_keywords(samp.body) for _ in range(SAMPLING_SIZE)]

    mean = samples[0].copy()
    for kw_idx in range(len(mean)):
        mean[kw_idx].score = math.median([s[kw_idx].score for s in samples])

    return mean


def generate():
    console.group('Keywords')

    for samp in get_samples():
        console.group(samp.name)

        file_comps = [samp.name, 'keywords']
        file_path = json_util.get_output_path(file_comps)

        try:
            received = get_mean_keywords(samp)
            keywords = sorted(received, reverse=True)
            keyword_count = sum([kw.count for kw in keywords])

            data = OrderedDict()
            data['keyword_count'] = keyword_count
            data['keywords'] = [dictify(kw) for kw in keywords]

            json_util.write(file_path, data, 'keywords')

            console.success('saved to: {}'.format(file_path))

        except Exception as e:
            console.error(e)
            console.info('deleting: {!r}'.format(file_path))

            json_util.cleanup(file_path)

        console.group_end()

    console.group_end()
