from .document import Document


class TextDocument(Document):
    def get_source(self, path: str):
        return self._get_source(path, False)

    def get_stream(self, path: str):
        return self._get_stream(path)
