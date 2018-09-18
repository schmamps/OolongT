"""Plain text document"""
from ..io import read_file
from ..typings import PathOrString
from .text_document import TextDocument


class PlainTextDocument(TextDocument):
    """Read text file as body of content"""
    def __init__(self, path: PathOrString) -> None:
        body = read_file(path)

        super().__init__(body, None, path)

    # pylint: disable=unused-argument
    @staticmethod
    def supports(path: str, ext: str) -> bool:
        return True
