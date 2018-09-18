"""Document-based content"""
import abc
import typing

from ..typings import OptionalString, PathOrString
from .content import Content


def norm_path(path: PathOrString) -> OptionalString:
    """Cast path as string or None

    Arguments:
        path {PathOrString} -- str or pathlib.Path to document

    Returns:
        OptionalString -- path as str, else None
    """
    if isinstance(path, str):
        return path

    return str(path) if path else None


class Document(Content):
    """Document subclass of Content"""
    @property
    def path(self) -> OptionalString:
        """Get path to document (if any)

        Returns:
            OptionalString -- path do document
        """
        return self._path

    def __init__(
            self,
            body: typing.Any,
            title: typing.Any,
            path: PathOrString) -> None:
        self._path = norm_path(path)
        super().__init__(body, title)

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
