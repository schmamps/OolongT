"""Text Content"""
import typing

from .content import Content


class TextContent(Content):
    """Implement Content for input text"""
    def __init__(self, body: str, title: str = '') -> None:
        super().__init__(body, title)

    @staticmethod
    def supports(_: typing.Any, __: typing.Any) -> bool:
        return True
