"""Test TextContent content class"""
import typing

from pytest import mark

from src.oolongt.content.text_content import TextContent
from test_content import TestContent
from tests.helpers import pad_to_longest
from tests.params.content import param_content_init, split_any

BODY = 'Content Body'
TITLE = 'Title Of Content'
REF_CONTENT = {'body': BODY, 'title': TITLE}


def get_init(keys: typing.Any):
    """Get initializing parameters for TextContent

    Arguments:
        keys {typing.Any} -- list of variables to init

    Returns:
        dict -- dictionary of initializing keyword args
    """
    requested_keys = split_any(keys)

    init = {
        key: REF_CONTENT[key]
        for key in ['body', 'title']
        if key in requested_keys}

    return init


# pylint: disable=no-self-use
class TestTextContent(TestContent):
    """Test TextContent subclass"""
    @mark.parametrize(
        'kwargs,expected',
        [
            (get_init('body'), (BODY, '')),
            (get_init('body,title'), (BODY, TITLE))],
        ids=pad_to_longest([
            'body-only',
            'body-title', ]))
    def test___init__(self, kwargs: dict, expected: tuple):
        """Test Content subclass initialization

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
