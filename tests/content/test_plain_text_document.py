"""Test PlainTextDcoument content class"""
from src.oolongt.content import PlainTextDocument
from test_text_document import TestTextDocument
from tests.params.content import (
    DOC_INIT_EXPECTED, param_document_init, param_supports)


class TestPlainTextDocument(TestTextDocument):
    @param_document_init(PlainTextDocument, 'txt', stems=['basic', 'intermed'])
    def test___init__(
            self, inst: PlainTextDocument, expected: DOC_INIT_EXPECTED):
        expected = (expected[0], '', expected[2])

        assert self.compare_document(inst, expected)

    @param_supports('txt', always=True)
    def test_supports(self, path, ext, expected):
        received = PlainTextDocument.supports(path, ext)

        assert received == expected
