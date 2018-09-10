"""Content extractor for MS Word files"""
from docx2txt import DocxFile

from ..io import get_stream
from ..typings import PathOrString
from .binary_document import BinaryDocument


class DocxDocument(BinaryDocument):
    """Parse Word XML"""
    def __init__(self, path: PathOrString) -> None:
        """Initialize for file at `path`
        Arguments:
            path {str} -- path to document
        """
        with get_stream(path) as stream:
            src = DocxFile(stream)

            body = src.main
            title = src.properties.get('title')

        super().__init__(body, title, path)

    # pylint: disable=unused-argument
    @staticmethod
    def supports(path: str, ext: str) -> bool:
        return ext == 'docx'
