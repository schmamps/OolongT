"""Test UglyQuery"""
import typing

from src.oolongt.content.content import norm_text
from src.oolongt.typings import OptionalString, StringList
from src.oolongt.ugly_soup.ugly_query import UglyQuery, get_text, list_tags
from tests.params.helpers import parametrize
from tests.params.ugly_soup import (
    SOUP, TEST_IDS, TEST_TAGS, param___repr__, param_get_text, param_test)


@param_get_text()
def test_get_text(tag: str, expected: str):
    """Test `get_text` in ugly_query subpackage

    Arguments:
        tag {str} -- HTML tag
        expected {str} -- expected text content
    """
    received = norm_text(get_text(SOUP(tag)[0]))

    assert received == expected


@parametrize('tag_list,expected,_,__', TEST_TAGS, TEST_IDS)
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
    @parametrize('args', TEST_TAGS, TEST_IDS)
    def test___init__(self, args: tuple):
        """Test `UglyQuery` initialization

        Arguments:
            args {tuple} -- it's... complicated
        """
        expected = (args[1], args[2])

        inst = UglyQuery(args[0], args[2])
        received = (inst.tags, inst._tester)

        assert received == expected

    @parametrize('args', TEST_TAGS, TEST_IDS)
    def test_tags(self, args: tuple):
        """Test `UglyQuery.tags` property

        Arguments:
            args {tuple} --
        """
        expected = args[1]

        inst = UglyQuery(args[0], args[2])
        received = inst.tags

        assert received == expected

    @parametrize('args', TEST_TAGS, TEST_IDS)
    def test_tester(self, args: tuple):
        """Test `UglyQuery.tester` property

        Arguments:
            args {tuple} --
        """
        expected = args[2]

        inst = UglyQuery(args[0], args[2])
        received = inst.tester

        assert received == expected

    @param_test()
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

    @param___repr__()
    def test___repr__(self, args):
        """Test `UglyQuery` REPR

        Arguments:
            args {tuple} --
        """
        expected = 'UglyQuery([\'div\'], {!r})'.format(norm_text)

        inst = UglyQuery(args, norm_text)
        received = repr(inst)

        assert received == expected
