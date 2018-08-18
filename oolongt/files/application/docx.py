"""Content extractor for MS Word files"""
import typing
from re import split

from docx2txt import DocxFile

from oolongt.typedefs import Content


def load(path: str) -> typing.Tuple:
    doc = DocxFile(path)
    body = doc.text
    title = doc.properties.get('Title', False)
    keywords = doc.properties.get('Keywords', '')

    return body, title, split(r'\s*,\s*', keywords)


def parse(path: str) -> Content:
    return Content(load, path)
