"""Test DocxDocument content class"""
from src.oolongt.content import DocxDocument
from test_binary_document import TestBinaryDocument
from tests.params.content import (
    DocumentInit, compare_document, param_document_init, param_supports)

STEMS = ['basic']
EXTENSION = 'docx'


class TestDocxDocument(TestBinaryDocument):
    """Test DocxDocument subclass"""
    @param_document_init(DocxDocument, EXTENSION, STEMS)
    def test___init__(self, inst: DocxDocument, expected: DocumentInit):
        assert compare_document(inst, expected)

    @param_supports(EXTENSION)
    def test_supports(self, path, ext, expected):
        assert self.supports(DocxDocument, path, ext, expected)

    @param_document_init(DocxDocument, EXTENSION, STEMS)
    def test___repr__(self, inst: DocxDocument, expected):
        assert self._test_doc_repr(inst, expected)
