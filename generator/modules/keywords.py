from oolongt.summarizer import Summarizer
from oolongt.parser import Parser
from oolongt.nodash import pluck

from generator.util import get_samples, json as json_util


def jsonify(keyword):
    data = {
        'score': keyword.score,
        'count': keyword.count,
        'word': keyword.word, }

    pairs = [
        json_util.kv_pair(data, 'score', '.12f'),
        json_util.kv_pair(data, 'count', '2d'),
        json_util.kv_pair(data, 'word'), ]

    return '\t\t{' + ', '.join(pairs) + '}'


def generate():
    p = Parser()

    for samp in get_samples():
        receiveds = p.get_keywords(samp.body)
        keywords = sorted(receiveds, reverse=True)
        word_count = sum([kw.count for kw in keywords])

        with json_util.create(samp.name, 'keywords') as file:
            file.write('{\n')
            file.write('\t"word_count": {0:d},\n'.format(word_count))
            file.write('\t"keywords": [\n')
            file.write(',\n'.join([jsonify(kw) for kw in keywords]))
            file.write(json_util.close(']'))

        # basic_words = [kw.word for kw in samp.keywords]
        # stem_words = [kw.word for kw in keywords]

        # if len(basic_words):
        #     for word in sorted(list(set(basic_words + stem_words))):
        #         if word not in basic_words and len(basic_words) > 0:
        #             print('unique stem: ' + word)

        #         if word not in stem_words:
        #             print('unique basic: ' + word)
        print('')
