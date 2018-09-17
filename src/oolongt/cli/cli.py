"""Command line interface for OolongT"""
import argparse
import os
import sys
import typing
from textwrap import wrap as wrap_text

from ..constants import DEFAULT_LENGTH
from ..content import Document
from ..files import get_document
from ..string import simplify
from ..typings import OptionalString, StringList

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


def get_summary(doc: Document, limit: float, wrap: int) -> StringList:
    """Get summary of `doc` as StringList of lines

    Arguments:
        doc {Document} -- document
        limit {float} -- length of summary
        wrap {int} -- column wrap

    Returns:
        StringList -- lines of document
    """
    sentences = doc.summarize(limit)
    text = ' '.join(sentences)

    return [text] if wrap < 1 else wrap_text(text, width=wrap)


def get_output_lines(
        path: str,
        ext: OptionalString,
        limit: float,
        wrap: int) -> typing.Generator[str, None, None]:
    """Generate lines of output

    Arguments:
        path {str} -- path to document
        ext {OptionalString} -- nominal extension of file
        limit {float} -- length of summary
        wrap {int} -- column wrap

    Returns:
        typing.Generator[str, None, None] -- output lines
    """
    doc = get_document(path, ext)

    yield simplify(doc.title or path)
    yield ''

    for line in get_summary(doc, limit, wrap):
        yield simplify(line)


def cli():
    """Collect arguments, pass for summary, output to console"""
    args = get_args()
    limit = float(args.limit)
    wrap = int(args.wrap)

    for line in get_output_lines(args.path, args.ext, limit, wrap):
        print(line)
