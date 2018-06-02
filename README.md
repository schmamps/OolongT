# OolongT

## About
OolongT is an automatic summarization algorithm
largely based on the official version of TextTeaser.
It is written with versatility, testability, simplicity,
and compatibility in mind.

TextTeaser links:
* [Python (current)](https://github.com/MojoJolo/textteaser)
* [Scala (original)](https://github.com/MojoJolo/textteaser)

## Getting started
```sh
#!/bin/sh
git clone https://github.com/schmamps/OolongT.git
pip install -r requirements.txt
```

## Basic Usage
```py
>>> from oolongt import summarize
...
>>> summarize(title, text)
['most important sentence', …, 'least important sentence']
```

## Configuration

…coming soon?

## Advanced Usage

For a list of *every* sentence in the source text, call:
`rank_sentences()` instead.

### Length
OolongT can reduce text to either a fixed number of sentences:
```py
>>> from oolongt import summarize
...
>>> summarize(title, text, length=2)
['most important sentence', '2nd most…']
```

…or a specific fraction of the original if `0 < length < 1`:
```py
>>> from oolongt import summarize
...
>>> text = '…'  # six sentences total
>>> summarize(title, text, length=.5)
['most important sentence', '2nd most…', 'third most…']
```


### Sorting
By default, OolongT sorts top sentences
by their order of appearance in ascending order

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

