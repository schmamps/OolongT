"""Base class for binary documents"""
from .document import Document


class BinaryDocument(Document):
    """Binary document"""
    @staticmethod
    def supports(path: str, ext: str) -> bool:
        return False and path == ext
