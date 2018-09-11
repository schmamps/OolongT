"""Test PdfDocument content class"""
from PyPDF2 import PdfFileReader
from pytest import mark

from src.oolongt.content import PdfDocument
from src.oolongt.content.pdf_document import get_body, get_page, get_title
from src.oolongt.io import get_stream
from test_binary_document import TestBinaryDocument
from tests.helpers import pad_to_longest
from tests.params.content import (
    DocumentInit, compare_document, get_doc_path, param_document_init,
    param_supports)

STEMS = ['basic']
SUBJECT = PdfDocument
EXTENSION = 'pdf'


def parametrize_basic(expected='Basic body'):
    """Parametrize tests for basic PDF

    Keyword Arguments:
        expected {str} -- expected body (default: {'Basic body'})

    Returns:
        test params -- test params
    """
    return mark.parametrize(
        'stem,expected',
        [('basic', expected)],
        ids=pad_to_longest(['basic']))


def get_path(stem: str) -> str:
    """Get path to sample named `stem`

    Arguments:
        stem {str} -- stem of sample path

    Returns:
        str -- full path to sample
    """
    return get_doc_path(stem, 'pdf')


@parametrize_basic()
def test_get_page(stem: str, expected: str):
    """Test get_page function of pdf_document

    Arguments:
        stem {str} -- stem of sample path
        expected {str} -- expected content
    """
    with get_stream(get_path(stem)) as stream:
        src = PdfFileReader(stream)

        received = get_page(src, 0).strip()

    assert received == expected


@parametrize_basic()
def test_get_body(stem: str, expected: str):
    """Test get_body function of pdf_document

    Arguments:
        stem {str} -- stem of sample path
        expected {str} -- expected content
    """
    with get_stream(get_path(stem)) as stream:
        src = PdfFileReader(stream)

        received = get_body(src).strip()

    assert received == expected


@parametrize_basic('Basic Title')
def test_get_title(stem: str, expected: str):
    """Test get_body function of pdf_document

    Arguments:
        name {str} -- stem of sample path
        expected {str} -- expected content
    """
    with get_stream(get_path(stem)) as stream:
        info = PdfFileReader(stream).getDocumentInfo()

        received = get_title(info).strip()

    assert received == expected


class TestPdfDocument(TestBinaryDocument):
    """Test PdfDocument subclass"""
    @param_document_init(SUBJECT, EXTENSION, STEMS)
    def test___init__(self, inst: PdfDocument, expected: DocumentInit):
        assert compare_document(inst, expected)

    @param_supports(EXTENSION, always=None)
    def test_supports(self, path, ext, expected):
        assert self.supports(SUBJECT, path, ext, expected)

    @param_document_init(SUBJECT, EXTENSION, STEMS)
    def test___repr__(self, inst, expected):
        assert self._test_doc_repr(inst, expected)
