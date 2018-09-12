"""Test `PlainTextDcoument` content class"""
from src.oolongt.content import PlainTextDocument
from test_text_document import TestTextDocument
from tests.params.content import (
    DocumentInit, compare_document, param_document_init, param_supports)

SUBJECT = PlainTextDocument
EXTENSION = 'txt'
STEMS = ['basic', 'intermed']


class TestPlainTextDocument(TestTextDocument):
    """Test `PlainTextDocument` content class"""
    @param_document_init(SUBJECT, EXTENSION, STEMS)
    def test___init__(
            self, inst: PlainTextDocument, expected: DocumentInit):
        expected = (expected[0], '', expected[2])

        assert compare_document(inst, expected)

    @param_supports(EXTENSION, always=True)
    def test_supports(self, path, ext, expected):
        assert self.supports(PlainTextDocument, path, ext, expected)

    @param_document_init(SUBJECT, EXTENSION, STEMS)
    def test___repr__(self, inst, expected):
        assert self._test_doc_repr(inst, (expected[0], '', expected[2]))
