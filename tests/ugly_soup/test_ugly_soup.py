"""Test UglySoup"""
import typing

from src.oolongt.content.content import norm_text
from src.oolongt.typings import StringList
from src.oolongt.ugly_soup import UglyQuery
from tests.params.ugly_soup import SOUP, param__query, param_query


# pylint: disable=no-self-use
class TestUglySoup:
    """Test UglySoup"""
    @param__query()
    def test__query(self, kwargs: dict, expected: typing.Any):
        """Test `UglyQuery.query`

        Arguments:
            kwargs {dict} -- initialization arguments
            expected {typing.Any} -- expected result
        """
        query = UglyQuery(**kwargs)
        result = SOUP._query(query)  # pylint: disable=protected-access
        received = norm_text(result) if isinstance(result, str) else result

        assert received == expected

    @param_query()
    def test_query(
            self,
            tags: StringList,
            kwargs: dict,
            expected: str):
        """Test `UglyQuery.query`

        Arguments:
            tags {StringList} -- list of tags
            kwargs {dict} -- initialization arguments
            expected {str} -- expected result
        """
        queries = [UglyQuery(tag_spec) for tag_spec in tags]
        received = norm_text(SOUP.query(*queries, **kwargs))

        assert received == expected
