import argparse
import os
import sys

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

    if not os.path.exists(args.path):
        sys.stderr.write('File {!r} does not exist.'.format(args.docx))
        sys.exit(1)

    return args


def get_output():
    args = get_args()

    return summarize(args.path, int(args.length))
