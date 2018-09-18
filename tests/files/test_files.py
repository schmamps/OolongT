"""Test files subpackage"""
from src.oolongt.files.files import get_document, get_handler
from src.oolongt.typings import OptionalString
from tests.params.content import compare_document
from tests.params.files import param_get_document, param_get_handler


@param_get_handler()
def test_get_handler(path: str, ext: OptionalString, expected: str):
    """Test `get_handler`

    Arguments:
        path {str} -- path to document
        ext {OptionalString} -- nominal extension of doc
        expected {str} -- name of handler class
    """
    kwargs = {
        key: val for key, val
        in {'path': path, 'ext': ext}.items()
        if val is not None}
    received = get_handler(**kwargs).__name__

    assert received == expected


@param_get_document()
def test_get_document(path: str, ext: OptionalString, expected: tuple):
    """Test `get_document`

    Arguments:
        path {str} -- path to document
        ext {OptionalString} -- nominal extension
        expected {tuple} -- expected document properties
    """
    received = get_document(path, ext)

    assert compare_document(received, expected)
