"""Test Content base content class"""
from src.oolongt.content.content import Content, norm_text
from src.oolongt.typings import OptionalString
from tests.params.content import (
    ContentInit, get_content, param_content, param_content_init,
    param_norm_text)


@param_norm_text()
def test_norm_text(text: OptionalString, expected: str):
    """Test norm_text

    Arguments:
        text {OptionalString} -- str or None
        expected {str} -- expected string
    """
    received = norm_text(text)

    assert received == expected


# pylint: disable=no-self-use
class TestContent:
    """Test Content class"""
    @param_content()
    def test_body(self, params: ContentInit, expected: tuple):
        """Test `body` property of instance

        Arguments:
            params {ContentInit} -- initialization params
            expected {tuple} -- expected body, title
        """
        inst = get_content(Content, params)

        assert inst.body == expected[0]

    @param_content()
    def test_title(self, params: ContentInit, expected: tuple):
        """Test `title` property of instance

        Arguments:
            params {ContentInit} -- initialization params
            expected {tuple} -- expected body, title
        """
        inst = get_content(Content, params)

        assert inst.title == expected[1]

    @param_content()
    def test___str__(self, params: ContentInit, expected: tuple):
        """Test string cast of instance

        Arguments:
            params {ContentInit} -- initialization params
            expected {tuple} -- expected body, title
        """
        inst = get_content(Content, params)

        assert str(inst) == expected[0]

    def _test_repr(self, inst: Content, expected: tuple):
        """Test REPR string of instance

        Arguments:
            inst {Content} -- initialization params
            expected {tuple} -- expected body, title
        """
        body, title = expected
        expected_str = '{}({!r}, {!r})'.format(
            inst.__class__.__name__, body, title)

        received = repr(inst)

        return received == expected_str

    @param_content_init(Content)
    def test___repr__(self, inst: Content, expected: tuple):
        """Test Content REPR

        Arguments:
            inst {Content} -- instance of Content
            expected {tuple} -- expected string
        """
        self._test_repr(inst, expected)
