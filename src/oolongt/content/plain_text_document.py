"""Plain text document"""
from ..io import get_contents
from ..typings import PathOrString
from .text_document import TextDocument


class PlainTextDocument(TextDocument):
    """Read text file as body of content"""
    def __init__(self, path: PathOrString) -> None:
        body = get_contents(path)

        self._initialize_document(body, None, path)

    # pylint: disable=unused-argument
    @staticmethod
    def supports(path: str, ext: str) -> bool:
        return True
