"""Test `TextContent` content class"""
from src.oolongt.content.text_content import TextContent
from test_content import TestContent
from tests.params.content import param_content_init, param_text_content_init


# pylint: disable=no-self-use
class TestTextContent(TestContent):
    """Test `TextContent` content class"""
    @param_text_content_init()
    def test___init__(self, kwargs: dict, expected: tuple):
        """Test `TextContent` initialization

        Arguments:
            kwargs {dict} -- initialization args
            expected {tuple} -- expected properties
        """
        inst = TextContent(**kwargs)
        received = (inst.body, inst.title)

        assert received == expected

    @param_content_init(TextContent)
    def test___repr__(self, inst, expected):
        assert self._test_repr(inst, expected)
