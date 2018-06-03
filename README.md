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
1. Install the required packages:
`pip install -r requirements.txt`
1. Setup a virtualenv (if necessary/desired)
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
* `nltk_language`: pass to NLTK tokenizer as named argument `language='…'`
* `ideal`: "ideal" sentence length, ostensibly 20 in English
* `stop_words`:
[words not important to content](https://en.wikipedia.org/wiki/Stop_words),
e.g. articles, pronouns
```js
{
	"meta": {
		"name": "German"
	},
	"nltk_language": "german",
	"ideal": 20,
	"stop_words": ["ein", "das", "die", "der", …]
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

If you wish to override the sort, the following keys are available:

* **`order`**: order of appearance in the text (default)
* `title_score`: frequency of words in the title
appearing in the sentence
* `keyword_score`: frequency of the most common keywords (significant words)
of the overall text appearing in the sentence
* `position_score`: score of the sentence based on
its location in the overall text
* `length_score`: closeness of the sentence to an ideal length
* `total_score`: overall score of the sentence
* `text`: text of the sentence

```py
>>> from oolongt import summarize
...
>>> summarize(title, text, length=3, sort_key='text')
['2nd most…', 'most important sentence', 'third most…']
```

If you wish to sort in descending order, pass `reverse=True`

```py
>>> from oolongt import summarize
...
>>> summarize(title, text, length=3, sort_key='text', reverse=True)
['third most…', 'most important sentence', '2nd most…' ]
```

