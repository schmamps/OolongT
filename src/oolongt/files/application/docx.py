"""Content extractor for MS Word files"""
import typing

from docx2txt import DocxFile

from oolongt.typedefs import Content


def load(path: str) -> typing.Dict[str, typing.Any]:
    doc = DocxFile(path)

    return {
        'body': doc.text,
        'title': doc.properties.get('Title'),
        'keywords': doc.properties.get('Keywords'), }


def parse(path: str) -> Content:
    return Content(load, path)
