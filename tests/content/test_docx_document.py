"""Test DocxDocument content class"""
from src.oolongt.content import DocxDocument
from test_binary_document import TestBinaryDocument
from tests.params.content import (
    DOC_INIT_EXPECTED, param_document_init, param_supports)


class TestDocxDocument(TestBinaryDocument):
    @param_document_init(DocxDocument, 'docx')
    def test___init__(self, inst: DocxDocument, expected: DOC_INIT_EXPECTED):
        assert self.compare_document(inst, expected)

    @param_supports('docx')
    def test_supports(self, path, ext, expected):
        received = DocxDocument.supports(path, ext)

        assert received == expected
