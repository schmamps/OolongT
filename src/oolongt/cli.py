import argparse
import os
import sys
from textwrap import wrap

from . import DEFAULT_LENGTH
from .files import summarize


def get_args():
    """Parse command line arguments if invoked directly

    Returns:
        object -- .img_dir: output directory, .details: get document details
    """
    desc = 'A Python-based utility to summarize content.'
    len_help = 'length of summary ({}, {}, [default: {}])'.format(
        '< 1: pct. of sentences', '>= 1: total sentences', DEFAULT_LENGTH)

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        'path', help='path to file')
    parser.add_argument(
        '-l', '--length', help=len_help, default=DEFAULT_LENGTH)

    args = parser.parse_args()

    if not args.path.startswith('http') and not os.path.exists(args.path):
        sys.stderr.write('File {!r} does not exist.'.format(args.path))
        sys.exit(1)

    return args


def get_summary(path: str, length: float):
    sentences, title = summarize(path, length)

    return ' '.join(sentences), title


def get_output():
    args = get_args()
    summary, title = get_summary(args.path, float(args.length))

    for line in [title, ''] + wrap(summary, width=79):
        print(line)
