"""Test UglySoup"""
import typing

from src.oolongt.content.content import norm_text
from src.oolongt.typings import StringList
from src.oolongt.ugly_soup import UglyQuery
from tests.params.ugly_soup import SOUP, param_query, param_query_sequence


# pylint: disable=no-self-use
class TestUglySoup:
    """Test UglySoup"""
    @param_query()
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

    @param_query_sequence()
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
