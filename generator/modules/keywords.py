from oolongt.summarizer import Summarizer
from oolongt.parser import Parser
from oolongt.nodash import pluck

from generator.util import get_samples, json as json_util


def jsonify(keyword):
    formatter = '\t\t{{"word": "{0}", "count": {1:d}, "total_score": {2:.8f}}}'
    return formatter.format(
        keyword['word'], keyword['count'], keyword['total_score'])


def generate():
    summ = Summarizer()
    p = Parser()

    for samp in get_samples():
        receiveds, word_count = p.get_keywords(samp.text)
        keywords = sorted(
            receiveds,
            key=lambda x: (-x['count'], x['word']))
        keywords = [summ.score_keyword(w, word_count) for w in keywords]

        with json_util.create(samp.name, 'keywords') as file:
            file.write('{\n')
            file.write('\t"word_count": {0:d},\n'.format(word_count))
            file.write('\t"keywords": [\n')
            file.write(',\n'.join([jsonify(kw) for kw in keywords]))
            file.write(json_util.close(']'))

        try:
            basic_words = pluck(samp.keywords or {}, 'word')

        except AttributeError:
            basic_words = []

        stem_words = pluck(keywords, 'word')

        if len(basic_words):
            for word in sorted(list(set(basic_words + stem_words))):
                if word not in basic_words and len(basic_words) > 0:
                    print('unique stem: ' + word)

                if word not in stem_words:
                    print('unique basic: ' + word)
        print('')
