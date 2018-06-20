from oolongt.summarizer import Summarizer

from generator.util import get_samples, json as json_util


def jsonify(sent):
    try:
        pairs = ',\n'.join([
            json_util.prop(sent, 'order', 'd'),
            json_util.prop(sent, 'sbs', '.8f'),
            json_util.prop(sent, 'dbs', '.8f'),
            json_util.prop(sent, 'title_score', '.8f'),
            json_util.prop(sent, 'length_score', '.8f'),
            json_util.prop(sent, 'position_score', '.2f'),
            json_util.prop(sent, 'keyword_score', '.8f'),
            json_util.prop(sent, 'total_score', '.8f'),
            json_util.prop(sent, 'text'),
            json_util.prop(sent, 'rank', 'd'),
        ])

        return '\t\t{\n' + pairs + '\n\t\t}'
    except (Exception):
        return


def generate():
    for samp in get_samples():
        summ = Summarizer()

        for samp in get_samples():
            receiveds = summ.get_sentences(
                samp.text, samp.title, None, None)

            by_score = sorted(receiveds, key=lambda x: -x['total_score'])
            for rank, _ in enumerate(by_score):
                by_score[rank]['rank'] = rank

            by_order = sorted(by_score, key=lambda x: x['order'])

            with json_util.create(samp.name, 'sentences') as file:
                file.write(json_util.open('sentences', '['))

                file.write(',\n'.join(
                    [jsonify(x) for x in by_order]
                ))

                file.write(json_util.close(']'))
