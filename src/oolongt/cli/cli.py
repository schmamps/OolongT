import argparse
import os
import sys
from textwrap import wrap as wrap_text

from ..constants import DEFAULT_LENGTH
from ..content import Document
from ..files import get_document
from ..typedef import OPT_STR, STR_LIST


DEFAULT_WRAP = 70


def get_args():
    """Parse command line arguments if invoked directly

    Returns:
        object -- .img_dir: output directory, .details: get document details
    """
    desc = 'A Python-based utility to summarize content.'
    limit_help = 'length of summary ({}, {}, [default: {}])'.format(
        '< 1: pct. of sentences', '>= 1: total sentences', DEFAULT_LENGTH)
    ext_help = 'nominal extension of file [default: {}]'.format(
        'txt if local, html if remote')
    wrap_help = 'wrap at column number [default: {}]'.format(
        DEFAULT_WRAP)

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        'path', help='path to file')
    parser.add_argument(
        '-e', '--ext', help=ext_help, default=None)
    parser.add_argument(
        '-w', '--wrap', help=wrap_help, default=DEFAULT_WRAP)
    parser.add_argument(
        '-l', '--limit', help=limit_help, default=DEFAULT_LENGTH)

    args = parser.parse_args()

    if not args.path.startswith('http') and not os.path.exists(args.path):
        sys.stderr.write('File {!r} does not exist.'.format(args.path))
        sys.exit(1)

    return args


def get_summary(doc: Document, limit: float, wrap: int) -> STR_LIST:
    sentences = doc.summarize(limit)
    text = ' '.join(sentences)

    return [text] if wrap < 1 else wrap_text(text, width=wrap)


def get_output_lines(path: str, ext: OPT_STR, limit: float, wrap: int):
    doc = get_document(path, ext)

    yield doc.title or path
    yield ''

    for line in get_summary(doc, limit, wrap):
        yield line


def cli():
    args = get_args()
    limit = float(args.limit)
    wrap = int(args.wrap)

    for line in get_output_lines(args.path, args.ext, limit, wrap):
        print(line)
