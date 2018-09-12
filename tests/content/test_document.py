"""Test `Document` base content class"""
from pathlib import Path

from pytest import mark

from src.oolongt.content.document import Document, norm_path
from src.oolongt.typings import PathOrString
from test_content import TestContent
from tests.helpers import pad_to_longest
from tests.params.content import (
    TEST_PATH, DocumentInit, get_document, param_document)

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


@mark.parametrize(
    'path,expected',
    [(__file__, __file__), (Path(__file__), __file__)],
    ids=pad_to_longest(['str', 'Path']))
def test_norm_path(path: PathOrString, expected: str):
    """Test `norm_path` path normalization

    Arguments:
        path {PathOrString} -- path to document
        expected {str} -- path as string
    """
    received = norm_path(path)

    assert received == expected


# pylint: disable=no-self-use
class TestDocument(TestContent):
    """Test `Document` content class"""
    @param_document()
    def test_path(self, params: DocumentInit, expected: tuple):
        """Test `Document.path` property

        Arguments:
            params {DocumentInit} -- initialization parameters
            expected {tuple} -- expected values
        """
        expected = TEST_PATH
        received = get_document(Document, params).path

        assert received == expected

    @mark.parametrize('inst,expected', [(None, None)], ids=['pass'])
    def test___init__(self, inst: Document, expected: DocumentInit):
        """Test `Document` initialization

        Arguments:
            inst {Document} -- instance of Document
            expected {DocumentInit} -- expected values
        """
        assert inst == expected

    def _test_doc_repr(self, inst: Document, expected: tuple) -> bool:
        """Test `Document` REPR

        Arguments:
            inst {Document} -- instance of Document (or subclass)
            expected {tuple} -- expected properties

        Returns:
            bool -- instance values are expected
        """
        body, title, path = expected
        expected_str = '{}({!r}, {!r}, {!r})'.format(
            inst.__class__.__name__, body, title, path)

        received = repr(inst)

        return received == expected_str

    def supports(self, cls, path, ext, expected):
        """Verify support for given `path` or file `ext`

        Arguments:
            path {str} -- path to document
            ext {str} -- nominal extension of document
            expected {bool} -- `path` or `ext` are supported

        Returns:
            bool -- .supports() == `expected`
        """
        return cls.supports(path, ext) == expected

    @mark.parametrize('path,ext,expected', [(None, None, None)], ids=['pass'])
    def test_supports(self, path, ext, expected):
        """Test `Document.supports` static method

        Arguments:
            path {PathOrString} -- path to document
            ext {str} -- nominal document extension
            expected {bool} -- `path` or `ext` are supported
        """
        assert path == ext == expected
