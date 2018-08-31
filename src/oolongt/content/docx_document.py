"""Content extractor for MS Word files"""
from docx2txt import DocxFile

from .binary_document import BinaryDocument


class DocxDocument(BinaryDocument):
    """Parse Word XML"""
    def get_source(self, path: str) -> DocxFile:
        """Get docx2txt object for file at `path`

        Arguments:
            path {str} -- path to document

        Returns:
            DocxFile -- docx2txt
        """
        return DocxFile(path)

    def __init__(self, path: str) -> None:
        """Initialize for file at `path`

        Arguments:
            path {str} -- [description]
        """
        src = self.get_source(path)

        body = self.get_body(src.main)
        title = src.properties.get('Title')
        keywords = src.properties.get('keywords')

        super().__init__(body, title, keywords, path)

    @staticmethod
    def supports(_: str, ext: str) -> bool:
        """Register support for given extension (path ignored)

        Arguments:
            _ {str} -- ignored
            ext {str} -- extension of document

        Returns:
            bool -- format is supported
        """
        return ext == 'docx'
