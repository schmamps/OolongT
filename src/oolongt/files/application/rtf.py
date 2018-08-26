"""Content extractor for RTF files"""
import typing

from oolongt.typedefs import Content


def load(path: str) -> typing.Dict[str, typing.Any]:
    return {}


def parse(path: str) -> Content:
    raise NotImplementedError('not implemented')

    return Content(load, path)  # pylint: disable=unreachable
