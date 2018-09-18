"""Text Content"""
from .content import Content


class TextContent(Content):
    """Implement Content for input text"""
    def __init__(self, body: str, title: str = '') -> None:
        super().__init__(body, title)
