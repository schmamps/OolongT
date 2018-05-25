TextTeaser
=============

TextTeaser is an automatic summarization algorithm.

This is not the official version of TextTeaser.

The official version of TextTeaser can be accessed
[here](https://github.com/MojoJolo/textteaser).

The original Scala TextTeaser can still be accessed
[here](https://github.com/MojoJolo/textteaser).


### Installation
    >>> git clone https://github.com/schmamps/textteaser.git
    >>> pip install -r requirements.txt

### How to Use
    >>> from textteaser import TextTeaser
    >>> tt = TextTeaser()
    >>> tt.summarize(title, text)

You can also test TextTeaser by running `python test.py`.
