"""Test BinaryDocument base content class"""
from src.oolongt.content import BinaryDocument
from test_document import TestDocument
from tests.params.content import param_document


class TestBinaryDocument(TestDocument):
    """Test BinaryDocument"""
    @param_document()
    def test___repr__(self, params, expected):
        self._test_repr(BinaryDocument, params, expected)
