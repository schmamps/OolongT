# OolongT

## About

OolongT is an automatic summarization algorithm
largely based on the official version of TextTeaser.
It is written with versatility, testability, and simplicity in mind.

TextTeaser links:

* [Python (current)](https://github.com/MojoJolo/textteaser)
* [Scala (original)](https://github.com/MojoJolo/textteaser)

## Install

For now, this package is most easily installed through git and setuptools.

```sh
# fetch repo
git clone https://github.com/schmamps/OolongT.git
cd OolongT
# install library
python setup.py install
# download NLTK data (follow prompts)
python setup.py nltk
```

## Basic Usage

### Procedural

For a simple summary of strings, call `summarize()`:

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

### Object Oriented

A few types of content are supported in `oolongt.content`.

Strings are supported with class `Content`.

```py
>>> from oolongt.content import Content
# ...
>>> cont = Content(text, title)
>>> cont.summarize()
["This is most important.", …, "This is fifth most important."]
```

## Working with Files

### Supported Types

The following file formats--local and remote--are also supported:

* Word XML (`DocxDocument`)
* HTML (`HtmlDocument`)
* PDF (`PdfDocument`)
* plain text (`PlainTextDocument`)

### Usage

```py
# Document is known format
>>> from oolongt.content import HtmlDocument
# ...
>>> doc = HtmlDocument('https://example.com/tldr.html')
>>> doc.summarize()
# ...
# Document is
```

### Command Line

When installed through setuptools,
the `oolongt` command is added to your system.

```sh
# get top two sentences at a given path/URL
$ oolongt -l 2 https://example.com/tldr
Title of Document

This is the first of the two best sentences in the document. This is
the other one.
```

## Advanced Usage

### Command Line

Arguments:

* `-h, --help`: help message
* `-e, --ext`: nominal extension of file (OolongT does no content sniffing and [defaults: `.txt` local, `.htm` remote)
* `-w, --wrap`  wrap at column number [default: 70]
* `-l, --limit`: [limit](#limit), i.e. length of summary

### Procedural/Object-Oriented

`score_body_sentences()` shadows `summarize()`
as a procedural function and method.
It returns a complete list of `ScoredSentence` objects.
The object has these properties:

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

### Keyword Arguments

Both `summarize` and `score_body_sentences`
take the same keyword arguments and use them (if applicable).

#### `limit`

By default, summaries are five sentences long (`len(summarize(...)) == 5`).
Use the `limit` argument to specify the number of sentences to return.
For values greater than or equal to 1,
this is an absolute number (maximum: all sentences).
For values between less than 1 but greater than 0,
it is a percentage (minimum: one sentence).

```py
# ...
>>> text = ["sentence 1 of 10", …, "sentence 10 of 10"]
>>> len(summarize(text, title, limit=3))
3
>>> len(summarize(text, title, limit=99))
10
>>> len(summarize(text, title, limit=.399))
4
>>> len(summarize(text, title, limit=.00399))
1
>>> len(summarize(text, title, limit=0))
ValueError
```

#### `root` and `idiom`

Specify a [custom idiom](#Idioms) with these arguments:

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
