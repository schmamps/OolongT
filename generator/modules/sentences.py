from oolongt.summarizer import Summarizer

from generator.util import get_samples, json as json_util


def jsonify(sent, rank):
    data = {
        'text': sent.text,
        'index': sent.index,
        'of': sent.of,
        'title_score': sent.title_score,
        'length_score': sent.length_score,
        'dbs_score': sent.dbs_score,
        'sbs_score': sent.sbs_score,
        'position_score': sent.position_score,
        'keyword_score': sent.keyword_score,
        'total_score': sent.total_score,
        'rank': rank, }

    pairs = ',\n\t\t\t'.join([
        json_util.kv_pair(data, 'index', 'd'),
        json_util.kv_pair(data, 'sbs_score', '.12f'),
        json_util.kv_pair(data, 'dbs_score', '.12f'),
        json_util.kv_pair(data, 'title_score', '.12f'),
        json_util.kv_pair(data, 'length_score', '.12f'),
        json_util.kv_pair(data, 'position_score', '.2f'),
        json_util.kv_pair(data, 'keyword_score', '.12f'),
        json_util.kv_pair(data, 'total_score', '.12f'),
        json_util.kv_pair(data, 'text'),
        json_util.kv_pair(data, 'rank', 'd'), ])

    return '\t\t{\n\t\t\t' + pairs + '\n\t\t}'


def generate():
    for samp in get_samples():
        summ = Summarizer()

        for samp in get_samples():
            receiveds = summ.get_sentences(
                samp.body, samp.title, None, None)
            ranks = [
                sent.index for sent in sorted(receiveds, reverse=True)]

            with json_util.create(samp.name, 'sentences') as file:
                file.write(json_util.open('sentences', '['))

                file.write(',\n'.join([
                    jsonify(sent, ranks.index(idx))
                    for idx, sent in enumerate(receiveds)]))

                file.write(json_util.close(']'))
