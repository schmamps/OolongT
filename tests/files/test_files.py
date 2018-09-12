"""Test files subpackage"""
import typing

from pytest import mark

from src.oolongt.files.files import get_document, get_handler
from src.oolongt.typings import OptionalString
from tests.helpers import pad_to_longest
from tests.params.content import (
    compare_document, get_doc_path, get_expected_doc)

GetDocParams = typing.Tuple[str, OptionalString, tuple]


def param_document(
        stem: str,
        ext: str,
        nominal_ext: OptionalString = None) -> GetDocParams:
    """Parametrize test_get_document

    Arguments:
        stem {str} -- stem of sample
        ext {str} -- extension of sample

    Keyword Arguments:
        nominal_ext {OptionalString} --
        nominal extension of doc (default: {None})

    Returns:
        GetDocParams -- path, ext, expected
    """
    path = get_doc_path(stem, ext)
    expected = get_expected_doc(stem, path)

    return (path, nominal_ext, expected)


@mark.parametrize(
    'path,ext,expected',
    [
        ('spam.html', None, 'HtmlDocument'),
        ('eggs.php', '.htm', 'HtmlDocument'),
        ('bacon.docx', None, 'DocxDocument'),
        ('ham.pdf', None, 'PdfDocument'),
        ('spam.foo', None, 'PlainTextDocument'), ],
    ids=pad_to_longest([
        'ext=html,handler=def.',
        'ext=docx,handler=def.',
        'ext=php,handler=def.',
        'ext=foo,handler=def.',
        'ext=php,handler=HTML', ]))
def test_get_handler(path: str, ext: OptionalString, expected: str):
    """Test `get_handler`

    Arguments:
        path {str} -- path to document
        ext {OptionalString} -- nominal extension of doc
        expected {str} -- name of handler class
    """
    kwargs = {
        key: val for key, val
        in {'path': path, 'ext': ext}.items()
        if val is not None}
    received = get_handler(**kwargs).__name__

    assert received == expected


@mark.parametrize(
    'path,ext,expected',
    [
        param_document('basic', 'html'),
        param_document('basic', 'pdf'),
        param_document('basic', 'php', 'html'), ],
    ids=pad_to_longest([
        'basic.htm',
        'basic.pdf',
        'basic.php']))
def test_get_document(path: str, ext: OptionalString, expected: tuple):
    """Test `get_document`

    Arguments:
        path {str} -- path to document
        ext {OptionalString} -- nominal extension
        expected {tuple} -- expected document properties
    """
    received = get_document(path, ext)

    assert compare_document(received, expected)
