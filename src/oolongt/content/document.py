import typing

from .content import Content
from ..simple_io import get_contents, get_stream


class Document(Content):
    def _get_source(self, path: str, binary: bool) -> typing.Any:
        return get_contents(path, binary)

    def _get_stream(self, path: str) -> typing.IO[typing.Any]:
        return get_stream(path)
