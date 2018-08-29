import typing

from bs4.element import Tag

from .repr_able import ReprAble


def get_text(tag: Tag) -> str:
    """Get text content of `tag`

    Arguments:
        tag {Tag} -- BeautifulSoup tag

    Returns:
        str -- text content
    """
    return tag.get_text().strip()


def list_tags(
        tags: typing.Union[str, typing.Sequence[str]]) -> typing.List[str]:
    """Expand tag list into formal typing.List of tag strings

    Arguments:
        tags {typing.Union[str, typing.Sequence[str]]} --
            list of tags as Sequence of strings or comma-delimited

    Returns:
        typing.List[str] -- [description]
    """
    raw_tags = tags.split(',') if isinstance(tags, str) else list(tags)
    final_tags = [str(tag).strip() for tag in raw_tags]

    return final_tags


class UglyQuery(ReprAble):
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
        self.tags = list_tags(tags)
        self._tester = tester

    def test(self, tag: Tag) -> typing.Union[str, None]:
        """Process tag, return content if found else None

        Arguments:
            tag {Tag} -- [description]

        Returns:
            typing.Union[str, None] -- [description]
        """
        return self._tester(tag)
