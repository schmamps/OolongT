"""Test PdfDocument content class"""
from PyPDF2 import PdfFileReader
from pytest import mark

from src.oolongt.content import PdfDocument
from src.oolongt.content.pdf_document import get_body, get_page, get_title
from src.oolongt.io import get_stream
from test_binary_document import TestBinaryDocument
from tests.constants import DOC_PATH
from tests.params.content import (
    DOC_INIT_EXPECTED, param_document_init, param_supports)


def parametrize(expected='Basic body'):
    return mark.parametrize(
        'name,expected',
        [('basic', expected)],
        ids=['basic'])


def get_path(name: str) -> str:
    return str(DOC_PATH.joinpath(name + '.pdf'))


def match_title(received: str, expected: str) -> bool:
    comp = received[:len(expected)].lower()

    return comp == expected


@parametrize()
def test_get_page(name, expected):
    with get_stream(get_path(name)) as stream:
        src = PdfFileReader(stream)

        received = get_page(src, 0).strip()

    assert received == expected


@parametrize()
def test_get_body(name, expected):
    with get_stream(get_path(name)) as stream:
        src = PdfFileReader(stream)

        received = get_body(src).strip()

    assert received == expected


@parametrize('Basic Title')
def test_get_title(name, expected):
    with get_stream(get_path(name)) as stream:
        info = PdfFileReader(stream).getDocumentInfo()

        received = get_title(info).strip()

    assert received == expected


class TestPdfDocument(TestBinaryDocument):
    @param_document_init(PdfDocument, 'pdf')
    def test___init__(self, inst: PdfDocument, expected: DOC_INIT_EXPECTED):
        assert self.compare_document(inst, expected)

    @param_supports('pdf', always=None)
    def test_supports(self, path, ext, expected):
        received = PdfDocument.supports(path, ext)

        assert received == expected
