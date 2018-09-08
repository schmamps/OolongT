"""Test TextContent content class"""
import typing

from pytest import mark

from src.oolongt.content.text_content import TextContent
from test_content import TestContent
from tests.helpers import pad_to_longest
from tests.params.content import split_any

BODY = 'Content Body'
TITLE = 'Title Of Content'
REF_CONTENT = {'body': BODY, 'title': TITLE}


def get_init(keys: typing.Any):
    requested_keys = split_any(keys)

    init = {
        key: REF_CONTENT[key]
        for key in ['body', 'title']
        if key in requested_keys}

    return init


class TestTextContent(TestContent):
    @mark.parametrize(
        'kwargs,expected',
        [
            (get_init('body'), (BODY, '')),
            (get_init('body,title'), (BODY, TITLE))],
        ids=pad_to_longest([
            'body-only',
            'body-title', ]))
    def test___init__(self, kwargs, expected):
        inst = TextContent(**kwargs)
        received = (inst.body, inst.title)

        assert received == expected
