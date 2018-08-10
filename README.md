# OolongT

## About

OolongT is an automatic summarization algorithm
largely based on the official version of TextTeaser.
It is written with versatility, testability, and simplicity in mind.

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

## Usage

### Basic

For a simple text summary, call `summarize()`:

```py
>>> from oolongt import summarize
# ...
>>> text = """All content text is here.
This is most important.
…
This is fifth most important.
…
This is the conclusion."""
>>> summarize(text, title)
["This is most important.", …, "This is fifth most important."]
```

*All* sentences, with additional data,
can be extracted by `score_body_sentences()`.
This function returns a list of `ScoredSentence` objects
with the following properties:

* `text`: text of the sentence
* `total_score`: composite of other sentence scores (comparison default)
* `index`: order of appearance in content (`sentences[index]`)
* `of`: total number of sentences in content (`len(sentences)`)
* `title_score`: score by keywords appearing in content title
* `length_score`: score by word count relative to `ideal` configuration
* `dbs_score`: score by keyword density
* `sbs_score`: score by summation
* `position_score`: score by position of sentence in content
* `keyword_score`: score by top keywords in content

### Advanced

Both `summarize` and `score_body_sentences`
take the same keyword arguments and use them (if applicable).

#### Keyword: `length`

By default, summaries are five sentences long (`len(summarize(...)) == 5`).
Use the `length` argument to specify the number of sentences to return.
For values greater than or equal to 1,
this is an absolute number (maximum: all sentences).
For values between less than 1 but greater than 0,
it is a percentage (minimum: one sentence).

```py
# ...
>>> text = ["sentence 1 of 10", …, "sentence 10 of 10"]
>>> len(summarize(text, title, length=3))
3
>>> len(summarize(text, title, length=99))
10
>>> len(summarize(text, title, length=.399))
4
>>> len(summarize(text, title, length=.00399))
1
>>> len(summarize(text, title, length=0))
ValueError
```

#### Keywords: `root` and `idiom`

Specify a [custom idiom](#Schema) with these arguments:

```py
>>> ...
>>> summarize(text, title, root="/etc/idioms")
# (results from configuration in "/etc/idioms/default.json")
>>> summarize(text, title, idiom="default")
# (results from configuration in "./oolongt/idioms/default.json")
>>> summarize(text, title, root="/etc/idioms", idiom="bsg")
# (results from configuration in "/etc/idioms/bsg.json")
```

## Idioms

OolongT uses "idioms" for configuration.
The default idiom is a generic setup for English,
largely based on [NLTK](https://www.nltk.org/) data,
including [stop words](https://en.wikipedia.org/wiki/Stop_words),
but this will not work for all content.

### Schema

If your content is not in English (but supported by NLTK)
or has a larger set of stop words,
you can specify this idiom with a JSON file:

```js
{
  "meta": {
    "name": "Battlestar Galactica Podcast Transcript"
  },
  "language": "english",
  "ideal": 20,
  "stop_words": {
    "nltk": true,
    "user": ["uh", "like", "frak", …]
  }
}
```

* `meta/name`: for reference only
* `language`: language parameter passed to NLTK
* `ideal`: "ideal" sentence length, ostensibly 20 in English
* `stop_words/nltk`: initialize with NLTK (true) or empty list (false)
* `stop_words/user`: supplemental stop words

### Programmatic Access

No API is provided to expose the parsing rules,
but the `parser` property of class `Summarizer` can be manipulated:

```py
>>> summarizer = Summarizer()
# ...
>>> text_de = "Dies ist eine furchtbare Ahnung. …Jetzt geht's los!"
>>> summarizer.parser.language = "german"
>>> summarizer.parser.stop_words = ["ein", "eine", …]
>>> sentences = summarizer.get_all_sentences(text_de, title_de, length=1)
["Dies ist eine furchtbare Ahnung."]
```
