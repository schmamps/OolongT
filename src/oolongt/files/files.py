"""Apply oolongt to files"""
import typing
from os.path import abspath
from pathlib import Path

import oolongt.text as main
from oolongt.constants import BUILTIN, DEFAULT_IDIOM, DEFAULT_LENGTH
from oolongt.typedefs import (Content, DocxDocument, HtmlDocument, PdfDocument,
                              PlainTextDocument, ScoredSentence)
from oolongt.typedefs.document import Document  # noqa


def get_handlers() -> typing.Generator[typing.Type[Document], None, None]:
    """List available document handlers

    Returns:
        Generator[Document, None, None] -- document handler
    """
    yield DocxDocument
    yield PdfDocument
    yield HtmlDocument


def get_handler(path: str, ext: str):
    """Determine which class to handle document

    Arguments:
        path {str} -- path/URL to document
        ext {str} -- override default extension

    Returns:
        typdefs.Document -- object with body, title, and keywords properties
    """
    ext = (ext or Path(path).suffix).replace('.', '')

    for handler in get_handlers():
        if handler.supports(path, ext):
            return handler

    return PlainTextDocument


def load_file(path: str, ext=False) -> Content:
    """Get text contents of the file at `path`

    Arguments:
        path {str} -- path to document

    Raises:
        ValueError -- unable to read file

    Returns:
        Content -- contents of file
    """
    handler = get_handler(path, ext)  # type: typing.Callable

    try:
        return handler(path)

    except (OSError) as e:  # pylint: disable=invalid-name
        raise ValueError('Unable to read {!r} ({})'.format(abspath(path), e))


def entitle(kwargs: typing.Dict[str, typing.Any]):
    """Get title from summarizer function args

    Arguments:
        kwargs {typing.Dict[str, typing.Any]} -- summarizing kwargs

    Returns:
        str -- document title
    """
    return kwargs.get('title', 'Untitled')


def prep_args(  # pylint: disable=too-many-arguments
        path: str,
        root: typing.Any,
        idiom: typing.Any,
        source: typing.Any,
        category: typing.Any,
        length: typing.Any = None) -> typing.Dict[str, typing.Any]:
    """Prepare arguments for passing to oolongt.text

    Arguments:
        path {str} -- path to document
        root {typing.Any} -- root of idiom directory
        idiom {typing.Any} -- name of idiom
        source {typing.Any} -- unused
        category {typing.Any} -- unused

    Keyword Arguments:
        length {typing.Any} --
            num/pct of sentences to return
            if applicable (default: {None})

    Returns:
        typing.Dict[str, typing.Any] -- keyword arguments for string functions
    """
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
        root: typing.Any = BUILTIN,
        idiom: typing.Any = DEFAULT_IDIOM,
        source=None,
        category=None) -> typing.Tuple[typing.List[ScoredSentence], str]:
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
    kwargs = prep_args(path, root, idiom, source, category)

    return main.score_body_sentences(**kwargs), entitle(kwargs)


def summarize(  # pylint: disable=too-many-arguments
        path: str,
        length: float = DEFAULT_LENGTH,
        root: typing.Any = BUILTIN,
        idiom: typing.Any = DEFAULT_IDIOM,
        source: typing.Any = None,
        category: typing.Any = None) -> typing.Tuple[typing.List[str], str]:
    """Get `length` best sentences from `body` in content order

    if `length` < 1:
        len(return) = int(length * len(sentences))
    else:
        len(return) = min(length, len(sentences))

    Arguments:
        body {str} -- body of content
        title {str} -- title of content

    Keyword Arguments:
        length {float} -- sentences to return (>= 1) or
            coefficient of total (< 1) (default: {oolongt.DEFAULT_LENGTH})
        root {str} -- root directory of idiom data
            (default: {oolongt.BUILTIN})
        idiom {str} -- basename of idiom file
            (default: {oolongt.DEFAULT_IDIOM})
        source {any} -- unused (default: {None})
        category {any} -- unused (default: {None})

    Returns:
        list[str] -- top sentences in content order
    """
    kwargs = prep_args(path, root, idiom, source, category, length)

    return main.summarize(**kwargs), entitle(kwargs)
