import typing

from . import Content
from ..simple_io import get_contents, get_stream


class Document(Content):
    # def get_remote(self, url: str, binary: bool) -> str:
    #     """[summary]

    #     Arguments:
    #         Content {[type]} -- [description]
    #         url {str} -- [description]
    #         binary {bool} -- [description]

    #     Returns:
    #         str -- [description]
    #     """

    #     headers = {'User-agent': 'Mozilla/5.0'}
    #     doc = requests.get(url, headers=headers)

    #     return doc.text if binary else doc.text

    # def get_local(self, path: str, binary: bool) -> typing.Union[bytes, str]:
    #     doc = get_contents(path, binary)

    #     return doc

    def _get_source(self, path: str, binary: bool) -> typing.Any:
        return get_contents(path, binary)

    def _get_stream(self, path: str) -> typing.IO[typing.Any]:
        return get_stream(path)
