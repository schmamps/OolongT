# OolongT

## About

OolongT is an automatic summarization algorithm
largely based on the official version of TextTeaser.
It is written with versatility, testability, simplicity,
and compatibility in mind.

TextTeaser links:

* [Python (current)](https://github.com/MojoJolo/textteaser)
* [Scala (original)](https://github.com/MojoJolo/textteaser)

## Setup

1. Download the repository from:
   <https://github.com/schmamps/OolongT.git>
1. `cd` to the project directory
1. Setup a virtualenv in `.venv` and activate (if necessary/desired)
1. Install the required packages:
   `pip install -r requirements.txt`
1. Run `python setup.py`
1. Follow the prompts to download NLTK data

## Basic Usage

```py
>>> from oolongt import summarize
...
>>> summarize(title, text)
['most important sentence', …, 'slightly less important sentence']
```

For a list of *every* sentence in the source text, call
`score_sentences()` instead.

## Advanced Usage

### Configuration

OolongT only knows (and defaults to) English as a language.
That language code (`lang`) is `'en'`.
If you wish to add to/override the builtin language(s),
you may specify an alternate language directory
using the named argument `root`.

```py
>>> from oolongt import summarize
...
>>> summarize(title, text, root='~/languages', lang='de')
[sentences tokenized by config in ~/languages/de.json]
```

#### Configuration File

* `meta/name`: for reference only
* `nltk_language`: name of language passed to NLTK
* `ideal`: "ideal" sentence length, ostensibly 20 in English
* `stop_words/nltk`: initialize the [stop word] list(https://en.wikipedia.org/wiki/Stop_words) from NLTK (`true`, default) or with an empty list (`false`)
* `stop_words/user`: list of stop words appended to the initial list

```js
{
  "meta": {
    "name": "Deutsch"
  },
  "nltk_language": "deutsch",
  "ideal": 20,
  "stop_words": {
    "nltk": true,
    "user": ["doch"]
  }
}
```

### Length

OolongT can reduce content to either a fixed number of sentences:

```py
>>> from oolongt import summarize
...
>>> summarize(title, text, length=2)
['most important sentence', '2nd most…']
```

…or a specific fraction of the original `if 0 < length < 1`:

```py
>>> from oolongt import summarize
...
>>> text = ['sentence one', 'sentence two', …, 'sentence six']
>>> summarize(title, text, length=.5)
['sentence one', 'sentence two', 'sentence three']
```

### Sorting

By default, OolongT sorts top sentences by their order of appearance.

For greater control over the quantity and order of sentences,
use the Summarizer class directly.
The `Summarizer.get_all_sentences` method parses content
and returns a list of `ScoredSentence` objects
with the following sortable properties:

* `total_score`: composite of other sentence scores (default)
* `index`: order of appearance in content
* `of`: total number of sentences in content
* `title_score`: score by keywords appearing in content title
* `length_score`: score by word count relative to `ideal` configuration
* `dbs_score`: score by keyword density
* `sbs_score`: score by summation
* `position_score`: score by position of sentence in content
* `keyword_score`: score by top keywords in content

```py
>>> from oolongt.summarizer import Summarizer
>>> Summarizer().get_all_sentences(body, title)
[ScoredSentence, ScoredSentence, ...]
```
