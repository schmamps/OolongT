"""File test parameters"""
import typing

from src.oolongt.typings import OptionalString
from tests.params.content import get_doc_path, get_expected_doc
from tests.params.helpers import parametrize

GetDocParams = typing.Tuple[str, OptionalString, tuple]


def get_info(
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


def param_get_document():
    """Parametrize `test_get_document`"""
    param_names = 'path,ext,expected'
    param_vals = (
        get_info('basic', 'html'),
        get_info('basic', 'pdf'),
        get_info('basic', 'php', 'html'),
    )
    ids = ('basic.htm', 'basic.pdf', 'basic.php')

    return parametrize(param_names, param_vals, ids)


def param_get_handler():
    """Parametrize test_get_handler"""
    param_names = 'path,ext,expected'
    param_vals = (
        ('spam.html', None, 'HtmlDocument'),
        ('eggs.php', '.htm', 'HtmlDocument'),
        ('bacon.docx', None, 'DocxDocument'),
        ('ham.pdf', None, 'PdfDocument'),
        ('spam.foo', None, 'PlainTextDocument'),
    )
    ids = (
        'ext=html,handler=def.',
        'ext=docx,handler=def.',
        'ext=php,handler=def.',
        'ext=foo,handler=def.',
        'ext=php,handler=HTML',
    )

    return parametrize(param_names, param_vals, ids)
