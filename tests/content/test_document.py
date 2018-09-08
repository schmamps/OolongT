"""Test Document base content class"""
from src.oolongt.content.document import Document
from test_content import TestContent
from tests.params.content import (
    DOC_INIT_EXPECTED, TEST_PATH, compare_document, get_document,
    param_document, param_supports)

EASY = {
    'path': 'dir/filename.ext',
    'stem': 'filename',
    'split': ['filename'],
    'entitle': ['Filename'],
    'title': 'Filename', }

HARD = {
    'path': 'dir/This,canned-SPAM ContainsPaté.webm',
    'stem': 'This,canned-SPAM ContainsPate',
    'split': ['This', 'canned', 'SPAM', 'Contains', 'Pate'],
    'entitle': ['This', 'Canned', 'SPAM', 'Contains', 'Pate'],
    'title': 'This Canned SPAM Contains Pate', }


class TestDocument(TestContent):
    """Test OolongT Document"""
    def compare_document(self, inst: Document, expected: DOC_INIT_EXPECTED):
        """Wrap around procedural compare_document

        Arguments:
            inst {Document} -- instance of Document
            expected {tuple} -- content body, title

        Returns:
            bool -- result is expected
        """
        return compare_document(inst, expected, expected[2])

    @param_document()
    def test_path(self, params, expected):
        expected = TEST_PATH
        received = get_document(Document, params).path

        assert received == expected

    def _test_repr(self, cls, params, expected):
        """Test repr() string of instance

        Arguments:
            params {tuple} -- initialization params
            expected {tuple} -- expected body, title
        """
        body, title = expected
        expected = '{}({!r}, {!r}, {!r})'.format(
           cls.__name__, body, title, TEST_PATH)

        inst = get_document(cls, params)
        received = repr(inst)

        assert received == expected

    @param_document()
    def test___repr__(self, params, expected):
        self._test_repr(Document, params, expected)

    @param_supports('', always=False)
    def test_supports(self, path, ext, expected):
        received = Document.supports(path, ext)

        assert received is False
