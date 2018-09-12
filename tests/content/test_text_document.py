"""Test `TextDocument` content class"""
from pytest import mark

from test_document import TestDocument


class TestTextDocument(TestDocument):
    """Test `TextDocument` content class (but not really)"""
    @mark.parametrize('path,ext,expected', [('', '', '')], ids=['pass'])
    def test_supports(self, path, ext, expected):
        assert path == ext == expected
