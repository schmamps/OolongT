import re
import typing
from os.path import abspath
from pathlib import Path

import magic

from oolongt import main
from oolongt.constants import BUILTIN, DEFAULT_IDIOM, DEFAULT_LENGTH
from oolongt.files import application, text
from oolongt.parser import Parser
from oolongt.summarizer import Summarizer
from oolongt.typedefs import Content, ScoredSentence


def get_mime_subtype(path: str) -> str:
    f = magic.Magic(mime=True, uncompress=True)
    mime = f.from_file(path)

    return mime.split('/').pop()


def load_file(path: str) -> Content:
    DOCX = '.'.join([
        'application/vnd',
        'openxmlformats-officedocument',
        'wordprocessingml',
        'document'])

    try:
        subtype = get_mime_subtype(path)
        func = None

        if subtype == 'msword':
            func = application.msword
        elif subtype == 'pdf':
            func = application.pdf
        elif subtype == 'rtf':
            func = application.rtf
        elif subtype == 'html':
            func = text.html
        elif subtype == 'plain':
            func = text.plain
        elif subtype == DOCX or path.endswith('.docx'):
            func = application.docx
        else:
            raise ValueError('unrecognized type: {!r}'.format(subtype))

        return func(path)

    except (IOError, FileNotFoundError, SyntaxError, ValueError) as e:
        raise IOError('Unable to read {!r} ({})'.format(abspath(path), e))


def prep_args(
        path: str,
        root: typing.Any,
        idiom: typing.Any,
        source: typing.Any,
        category: typing.Any,
        length: typing.Any
        ) -> typing.Dict[str, typing.Any]:
    content = load_file(path)

    nominal_args = {
        'body': content.body,
        'title': content.title,
        'root': root,
        'idiom': idiom,
        'source': source,
        'category': category,
        'length': length, }

    return {
        key: val
        for key, val in nominal_args.items()
        if val is not None}


def score_body_sentences(
        path: str,
        root: typing.Any = None,
        idiom: typing.Any = None,
        source: typing.Any = None,
        category: typing.Any = None,
        length: typing.Any = None
        ) -> typing.List[ScoredSentence]:
    """List and score every sentence in `body`

    Arguments:
        body {str} -- body of content
        title {str} -- title of content

    Keyword Arguments:
        root {str} -- root directory of idiom config
        idiom {str} -- basename of idiom config
        source {any} -- unused (default: {None})
        category {any} -- unused (default: {None})

    Returns:
        typing.List[ScoredSentence] --
            List of sentences with scoring and metadata
    """
    kwargs = prep_args(path, root, idiom, source, category, length)

    return main.score_body_sentences(**kwargs)


def summarize(
        path: str,
        length: float = DEFAULT_LENGTH,
        root: typing.Any = None,
        idiom: typing.Any = None,
        source: typing.Any = None,
        category: typing.Any = None
        ) -> typing.List[str]:
    """Get `length` best sentences from `body` in content order

    if `length` < 1:
        len(return) = int(length * len(sentences))
    else:
        len(return) = min(length, len(sentences))

    Arguments:
        body {str} -- body of content
        title {str} -- title of content

    Keyword Arguments:
        length {float} -- sentences to return (int) or
            fraction of total (float) (default: {5})
        root {str} -- root directory of idiom data
            (default: {parser.BUILTIN})
        idiom {str} -- basename of idiom file
            (default: {parser.DEFAULT_IDIOM})
        source {any} -- unused (default: {None})
        category {any} -- unused (default: {None})

    Returns:
        list[str] -- top sentences in content order
    """
    kwargs = prep_args(path, root, idiom, source, category, length)

    return main.summarize(**kwargs)
