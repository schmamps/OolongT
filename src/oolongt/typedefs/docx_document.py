"""Content extractor for MS Word files"""
from docx2txt import DocxFile

from .binary_document import BinaryDocument


class DocxDocument(BinaryDocument):
    def get_source(self, path: str) -> DocxFile:
        return DocxFile(path)

    def __init__(self, path: str) -> None:
        src = self.get_source(path)

        body = self.get_body(src.main)
        title = src.properties.get('Title')
        keywords = src.properties.get('Keywords')

        super().__init__(body, title, keywords, path)

    @staticmethod
    def supports(_: str, ext: str) -> bool:
        return ext == 'docx'
