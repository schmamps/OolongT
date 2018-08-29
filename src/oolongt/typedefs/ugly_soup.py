import typing

from bs4 import BeautifulSoup

from .ugly_query import UglyQuery


class UglySoup(BeautifulSoup):
    def query(self, query: UglyQuery) -> typing.Union[str, None]:
        """Execute a single UglyQuery on soup

        Arguments:
            query {UglyQuery} -- an UglyQuery

        Returns:
            typing.Union[str, None] -- str if found, None if no match
        """
        for tag in self(query.tags):
            val = query.test(tag)

            if val is not None:
                return val

        return None

    def query_sequence(
            self,
            queries: typing.Sequence[UglyQuery],
            default='') -> str:
        """Find first match in sequence of UglyQuery objects

        Arguments:
            queries {typing.Sequence[UglyQuery]} -- list of UglyQuery objects

        Keyword Arguments:
            path {str} -- path to document (default: {''})
            default {str} -- return string on failure (default: {''})

        Returns:
            str -- result of queries
        """
        for query in queries:
            result = self.query(query)

            if result is not None:
                return result

        return default
