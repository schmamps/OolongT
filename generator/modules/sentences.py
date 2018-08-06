from collections import OrderedDict

from oolongt.summarizer import Summarizer

from generator.util import console, get_samples, json as json_util, math


SAMPLE_SIZE = 25


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


def get_median_sentences(samp):
    summ = Summarizer()
    all_samples = [
        summ.get_all_sentences(samp.body, samp.title, None, None)
        for _ in range(SAMPLE_SIZE)]

    mean = all_samples[0].copy()
    for sent_idx in range(len(mean)):
        mean[sent_idx] = get_median_sentence(all_samples, sent_idx)

    return mean


def generate():
    console.group('Sentences')
    for samp in get_samples():
        console.group(samp.name)

        file_comps = [samp.name, 'sentences']
        file_path = json_util.get_output_path(file_comps)

        try:
            receiveds = get_median_sentences(samp)
            ranks = [
                sent.index for sent in sorted(receiveds, reverse=True)]

            data = OrderedDict()
            data['sentences'] = [
                dictify(sent, ranks.index(idx))
                for idx, sent in enumerate(receiveds)]

            json_util.write(file_path, data)

            console.success('saved to: {}'.format(file_path))

        except Exception as e:
            console.error(e)
            console.info('deleting: {!r}'.format(file_path))

            json_util.cleanup(file_path)

        console.group_end()

    console.group_end()
