"""Content extractor for MS Word files"""
from docx2python import docx2python

from ..typings import PathOrString
from .binary_document import BinaryDocument


class DocxDocument(BinaryDocument):
    """Parse Word XML"""
    def __init__(self, path: PathOrString) -> None:
        doc = docx2python(path)
        body = doc.text
        title = doc.properties.get('title', '')

        super().__init__(body, title, path)

    # pylint: disable=unused-argument
    @staticmethod
    def supports(path: str, ext: str) -> bool:
        return ext == 'docx'
