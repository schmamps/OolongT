import abc
import typing

from ..typedef import OPT_STR, PATH_STR
from .content import Content


def norm_path(path: PATH_STR) -> OPT_STR:
    """Cast path as string or None

    Arguments:
        path {PATH_STR} -- str or pathlib.Path to document

    Returns:
        OPT_STR -- path as str, else None
    """
    if isinstance(path, str):
        return path

    return str(path) if path else None


class Document(Content):
    @property
    def path(self) -> OPT_STR:
        """Get path to document (if any)

        Returns:
            OPT_STR -- path do document
        """
        return self._path

    def _initialize_document(
            self,
            body: typing.Any,
            title: typing.Any,
            path: PATH_STR):
        self._path = norm_path(path)
        self._initialize_content(body, title)

    def __init__(
            self,
            body: typing.Any,
            title: typing.Any,
            path: PATH_STR) -> None:
        self._initialize_document(body, title, path)

    def __repr__(self) -> str:
        return self._repr_(
            self.body, self.title, self.path)

    # pylint: disable=unused-argument
    @staticmethod
    @abc.abstractmethod
    def supports(path: str, ext: str) -> bool:
        """Claim support for a given path/extension

        Arguments:
            path {str} -- full path/URL of file
            ext {str} -- nominal extension of file

        Returns:
            bool -- path/extension are supported
        """
        return False
