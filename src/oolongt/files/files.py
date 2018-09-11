"""Apply oolongt to files"""
import typing
from os.path import abspath
from pathlib import Path

from ..content import (
    Document, DocxDocument, HtmlDocument, PdfDocument, PlainTextDocument)
from ..typings import OptionalString


def get_handlers() -> typing.Generator[typing.Type[Document], None, None]:
    """List available document handlers

    Returns:
        Generator[Document, None, None] -- document handler
    """
    yield DocxDocument
    yield PdfDocument
    yield HtmlDocument


def get_handler(path: str, ext: OptionalString = None) -> typing.Callable:
    """Determine which class to handle document

    TODO: use libmagic and/or MIME type from remote files

    Arguments:
        path {str} -- path/URL to document
        ext {str} -- override default extension ([Default: None])

    Returns:
        typdefs.Document -- object with body, title, and keywords properties
    """
    ext = (ext or Path(path).suffix).replace('.', '')

    for handler in get_handlers():
        if handler.supports(path, ext):
            return handler

    return PlainTextDocument


def get_document(path: str, ext: OptionalString) -> Document:
    """Get text contents of the file at `path`

    Arguments:
        path {str} -- path to document

    Raises:
        ValueError -- unable to read file

    Returns:
        Content -- contents of file
    """
    try:
        handler = get_handler(path, ext)
        doc = handler(path)  # type: Document

        return doc

    except (OSError) as e:  # pylint: disable=invalid-name
        raise ValueError('Unable to read {!r} ({})'.format(abspath(path), e))
