from generator.modules import keywords, sentences, merge
from generator.util import console

console.group('Sample Data Generator')

keywords.generate()
sentences.generate()
merge.generate()

console.group_end()
