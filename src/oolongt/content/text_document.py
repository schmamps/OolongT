"""Base class for text documents"""
from .document import Document


class TextDocument(Document):
    """Text document"""
    @staticmethod
    def supports(path: str, ext: str) -> bool:
        return False and path == ext
