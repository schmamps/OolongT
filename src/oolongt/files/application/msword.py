"""Content extractor for legacy MS Word files"""
import typing

from oolongt.typedefs import Content


def load(path: str) -> typing.Dict[str, typing.Any]:
    """Load Word .doc and extract properties

    Arguments:
        path {str} -- path to document

    Returns:
        typing.Dict[str, typing.Any] -- {body: str, title: str, keywords: Any}
    """
    return {'title': path}


def parse(path: str) -> Content:
    """Get content of document at `path`

    Arguments:
        path {str} -- path to document

    Returns:
        Content -- text properties of document
    """
    raise NotImplementedError('not implemented')

    return Content(load, path)  # pylint: disable=unreachable
