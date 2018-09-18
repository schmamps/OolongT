"""Content query for BeautifulSoup"""
from bs4 import BeautifulSoup

from ..typings import OptionalString
from .ugly_query import UglyQuery


# pylint: disable=abstract-method
class UglySoup(BeautifulSoup):
    """Add query features to BS4"""
    def _query(self, query: UglyQuery) -> OptionalString:
        """Execute a single UglyQuery on soup

        Arguments:
            query {UglyQuery} -- an UglyQuery

        Returns:
            OptionalString -- str if found, None if no match
        """
        for tag in self(query.tags):
            val = query.test(tag)

            if val is not None:
                return val

        return None

    def query(
            self,
            *queries: UglyQuery,
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
            result = self._query(query)

            if result is not None:
                return result

        return default

    def __init__(self, html: str, *args, **kwargs) -> None:
        init_kwargs = {'features': 'html.parser'}
        init_kwargs.update(kwargs)

        super().__init__(html, *args, **init_kwargs)
