"""Test UglySoup"""
import typing

from pytest import mark

from src.oolongt.content.content import norm_text
from src.oolongt.typings import StringList
from src.oolongt.ugly_soup import UglyQuery
from tests.helpers import pad_to_longest, return_true
from tests.params.ugly_soup import DOC, SOUP


# pylint: disable=no-self-use
class TestUglySoup:
    """Test UglySoup"""
    @mark.parametrize(
        'kwargs,expected',
        [
            ({'tags': 'div'}, None),
            ({'tags': 'div, main'}, DOC['body']),
            ({'tags': 'div, main', 'tester': return_true}, True)],
        ids=pad_to_longest(['none', 'text', 'func']))
    def test_query(self, kwargs: dict, expected: typing.Any):
        """Test `UglyQuery.query`

        Arguments:
            kwargs {dict} -- initialization arguments
            expected {typing.Any} -- expected result
        """
        query = UglyQuery(**kwargs)
        result = SOUP.query(query)
        received = norm_text(result) if isinstance(result, str) else result

        assert received == expected

    @mark.parametrize(
        'tags,kwargs,expected',
        [
            (['div'], {}, ''),
            (['div'], {'default': 'spam'}, 'spam'),
            (['div', 'main', 'header'], {'default': 'spam'}, DOC['body']), ],
        ids=pad_to_longest(['use-default', 'set-default', 'find-value']))
    def test_query_sequence(
            self,
            tags: StringList,
            kwargs: dict,
            expected: str):
        """Test `UglyQuery.query_sequence`

        Arguments:
            tags {StringList} -- list of tags
            kwargs {dict} -- initialization arguments
            expected {str} -- expected result
        """
        queries = [UglyQuery(tag_spec) for tag_spec in tags]
        received = norm_text(SOUP.query_sequence(*queries, **kwargs))

        assert received == expected
