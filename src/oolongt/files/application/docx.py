"""Content extractor for MS Word files"""
import typing

from docx2txt import DocxFile

from oolongt.typedefs import Content


def load(path: str) -> typing.Dict[str, typing.Any]:
    """Load Word XML and extract properties

    Arguments:
        path {str} -- path to document

    Returns:
        typing.Dict[str, typing.Any] -- {body: str, title: str, keywords: Any}
    """
    doc = DocxFile(path)

    return {
        'body': doc.main,
        'title': doc.properties.get('Title'),
        'keywords': doc.properties.get('Keywords'), }


def parse(path: str) -> Content:
    """Get content of document at `path`

    Arguments:
        path {str} -- path to document

    Returns:
        Content -- text properties of document
    """
    return Content(load, path)
