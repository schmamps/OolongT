"""Test UglyQuery"""
import typing

from bs4 import BeautifulSoup
from pytest import mark

from src.oolongt.simple_io import get_contents
from src.oolongt.ugly_query import UglyQuery, get_text, list_tags
from tests.constants import DOC_PATH
from tests.helpers import pad_to_longest, return_false, return_true

MARKUP = get_contents(DOC_PATH.joinpath('intermed.html'))
SOUP = BeautifulSoup(MARKUP, features='html.parser')
BODY_DIV_P = ['body', 'div', 'p']
TEST_TAGS = [
    (BODY_DIV_P, BODY_DIV_P, return_true, True),
    ([' body', ' div ', ' p'], BODY_DIV_P, return_false, False),
    ('body,div,p', BODY_DIV_P, return_true, True),
    ('body, div, p', BODY_DIV_P, return_false, False),
    (' body, div ,  p', BODY_DIV_P, return_true, True), ]
TEST_IDS = pad_to_longest([
    'simple-list-true',
    'sloppy-list-false',
    'simple-str-true',
    'comfy-str-false',
    'sloppy-str-true'])


@mark.parametrize(
    'tag,expected',
    [
        ('header', 'Header'),
        ('main', 'Body'),
        ('footer', 'Footer'), ],
    ids=pad_to_longest(['header', 'main', 'footer']))
def test_get_text(tag: str, expected: str):
    received = get_text(SOUP(tag)[0])

    assert received == expected


@mark.parametrize('tag_list,expected,_,__', TEST_TAGS, ids=TEST_IDS)
def test_list_tags(tag_list: typing.Any, expected: typing.List[str], _, __):
    received = list_tags(tag_list)

    assert received == expected


class TestUglyQuery:
    @mark.parametrize(
        'args',
        TEST_TAGS,
        ids=TEST_IDS)
    def test___init__(self, args):
        expected = (args[1], args[2])

        inst = UglyQuery(args[0], args[2])
        received = (inst.tags, inst._tester)

        assert received == expected

    @mark.parametrize(
        'tags,tester,expected',
        [
            ('main', get_text, 'Body'),
            ('style', get_text, None),
            ('input', get_text, None)],
        ids=pad_to_longest(['main', 'style', 'input']))
    def test_test(self, tags, tester, expected):
        inst = UglyQuery(tags, tester)
        results = SOUP(tags)

        received = None if len(results) < 1 else inst.test(results[0])

        assert received == expected
