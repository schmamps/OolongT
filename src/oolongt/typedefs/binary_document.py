import typing

from .document import Document


class BinaryDocument(Document):
    def get_source(self, path: str) -> typing.Any:
        return self._get_source(path, True)

    def get_stream(self, path: str) -> typing.Any:
        return self._get_stream(path, True)
