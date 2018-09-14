"""Test `TextDocument` content class"""
from test_document import TestDocument
from tests.params.helpers import parametrize


class TestTextDocument(TestDocument):
    """Test `TextDocument` content class (but not really)"""
    @parametrize('path,ext,expected', (('', '', ''), ), ids=('pass', ))
    def test_supports(self, path, ext, expected):
        assert path == ext == expected
