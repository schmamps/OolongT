"""Query into UglySoup"""
import typing

from bs4.element import Tag

from ..repr_able import ReprAble
from ..typings import OptionalString, StringList


def get_text(tag: Tag) -> str:
    """Get text content of `tag`

    Arguments:
        tag {Tag} -- BeautifulSoup tag

    Returns:
        str -- text content
    """
    return tag.get_text().strip()


def list_tags(
        tags: typing.Union[str, typing.Sequence[str]]) -> StringList:
    """Expand tag list into formal typing.List of tag strings

    Arguments:
        tags {typing.Union[str, typing.Sequence[str]]} --
            list of tags as Sequence of strings or comma-delimited

    Returns:
        StringList -- list of tags
    """
    raw_tags = tags.split(',') if isinstance(tags, str) else list(tags)
    final_tags = [str(tag).strip() for tag in raw_tags]

    return final_tags


# pylint: disable=too-few-public-methods
class UglyQuery(ReprAble):
    """Query data for UglySoup"""
    def __init__(
            self,
            tags: typing.Union[str, typing.Sequence[str]],
            tester: typing.Callable = get_text) -> None:
        """Initialize query

        Arguments:
            tags {typing.Union[str, typing.Sequence[str]]} -- tags to query

        Keyword Arguments:
            tester {typing.Callable} -- tag tester (default: {get_text})
        """
        self._tags = list_tags(tags)
        self._tester = tester

    @property
    def tags(self) -> StringList:
        """List query tags

        Returns:
            StringList -- list of tags
        """
        return self._tags

    @property
    def tester(self) -> typing.Callable:
        """Get query test function

        Returns:
            typing.Callable -- test function
        """
        return self._tester

    def test(self, tag: Tag) -> OptionalString:
        """Process tag, return content if found else None

        Arguments:
            tag {Tag} -- BeautifulSoup Tag object

        Returns:
            OptionalString -- content or None
        """
        return self._tester(tag)

    def __repr__(self):
        return self._repr_(self.tags, self._tester)
