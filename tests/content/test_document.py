"""Test `Document` base content class"""
from src.oolongt.content.document import Document, norm_path
from src.oolongt.typings import PathOrString
from test_content import TestContent
from tests.params.content import (
    TEST_PATH, DocumentInit, get_document, param_document, param_norm_path)
from tests.params.helpers import parametrize


@param_norm_path()
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

    @parametrize('inst,expected', ((None, None), ), ('pass', ))
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

    @parametrize('path,ext,expected', ((None, None, None), ), ('pass', ))
    def test_supports(self, path, ext, expected):
        """Test `Document.supports` static method

        Arguments:
            path {PathOrString} -- path to document
            ext {str} -- nominal document extension
            expected {bool} -- `path` or `ext` are supported
        """
        assert path == ext == expected
