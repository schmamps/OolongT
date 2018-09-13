"""Test UglyQuery"""
import typing

from pytest import mark

from src.oolongt.content.content import norm_text
from src.oolongt.typings import OptionalString, StringList
from src.oolongt.ugly_soup.ugly_query import UglyQuery, get_text, list_tags
from tests.helpers import pad_to_longest, return_false, return_true
from tests.params.ugly_soup import DOC, SOUP

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
        ('main', DOC['body']),
        ('footer', 'Footer'), ],
    ids=pad_to_longest(['header', 'main', 'footer']))
def test_get_text(tag: str, expected: str):
    """Test `get_text` in ugly_query subpackage

    Arguments:
        tag {str} -- HTML tag
        expected {str} -- expected text content
    """
    received = norm_text(get_text(SOUP(tag)[0]))

    assert received == expected


@mark.parametrize('tag_list,expected,_,__', TEST_TAGS, ids=TEST_IDS)
def test_list_tags(tag_list: typing.Any, expected: StringList, _, __):
    """Test `list_tags` in ugly_query subpackage

    Arguments:
        tag_list {typing.Any} -- list of tags
        expected {StringList} -- expected tags
        _ {typing.Any} -- ignored
        __ {typing.Any} -- ignored
    """
    received = list_tags(tag_list)

    assert received == expected


# pylint: disable=no-self-use,protected-access
class TestUglyQuery:
    """Test UglyQuery"""
    @mark.parametrize('args', TEST_TAGS, ids=TEST_IDS)
    def test___init__(self, args: tuple):
        """Test `UglyQuery` initialization

        Arguments:
            args {tuple} -- it's... complicated
        """
        expected = (args[1], args[2])

        inst = UglyQuery(args[0], args[2])
        received = (inst.tags, inst._tester)

        assert received == expected

    @mark.parametrize('args', TEST_TAGS, ids=TEST_IDS)
    def test_tags(self, args: tuple):
        """Test `UglyQuery.tags` property

        Arguments:
            args {tuple} --
        """
        expected = args[1]

        inst = UglyQuery(args[0], args[2])
        received = inst.tags

        assert received == expected

    @mark.parametrize('args', TEST_TAGS, ids=TEST_IDS)
    def test_tester(self, args: tuple):
        """Test `UglyQuery.tester` property

        Arguments:
            args {tuple} --
        """
        expected = args[2]

        inst = UglyQuery(args[0], args[2])
        received = inst.tester

        assert received == expected

    @mark.parametrize(
        'tags,tester,expected',
        [
            ('main', get_text, DOC['body']),
            ('style', get_text, None),
            ('input', get_text, None)],
        ids=pad_to_longest(['main', 'style', 'input']))
    def test_test(
            self,
            tags: typing.Any,
            tester: typing.Callable,
            expected: OptionalString):
        """Test `UglyQuery.test` method

        Arguments:
            tags {typing.Any} -- list of tags
            tester {typing.Callable} -- testing function
            expected {OptionalString} -- expected result
        """
        inst = UglyQuery(tags, tester)
        results = SOUP(tags)

        received = None if not results else norm_text(inst.test(results[0]))

        assert received == expected

    @mark.parametrize(
        'args',
        [('div')],
        ids=pad_to_longest(['basic']))
    def test___repr__(self, args):
        """Test `UglyQuery` REPR

        Arguments:
            args {tuple} --
        """
        expected = 'UglyQuery([\'div\'], {!r})'.format(norm_text)

        inst = UglyQuery(args, norm_text)
        received = repr(inst)

        assert received == expected
