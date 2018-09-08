"""Test HtmlDocument content class"""
from pytest import mark

from src.oolongt.content import HtmlDocument
from src.oolongt.content.content import norm_text
from src.oolongt.content.html_document import (
    get_body, get_og_title, get_title, process)
from src.oolongt.io import get_contents
from src.oolongt.ugly_soup import UglySoup
from test_text_document import TestTextDocument
from tests.constants import DOC_PATH
from tests.params.content import (
    DOC_INIT_EXPECTED, param_document_init, param_supports)

BASIC_INTERMED = [('basic'), ('intermed')]


def get_path(name: str) -> str:
    return str(DOC_PATH.joinpath(name + '.html'))


def get_html(name: str) -> str:
    path = get_path(name)
    return get_contents(path)


def get_soup(name: str) -> UglySoup:
    html = get_html(name)
    return UglySoup(html)


@mark.parametrize('name', BASIC_INTERMED)
def test_process(name):
    expected = UglySoup

    html = get_html(name)
    received = process(html)

    assert isinstance(received, expected)


@mark.parametrize('name', BASIC_INTERMED)
def test_get_body(name: str):
    expected = '{} body'.format(name.title())

    src = get_soup(name)
    received = norm_text(get_body(src))

    assert received == expected


@mark.parametrize(
    'tag,expected',
    [
        ({}, None),
        ({'property': 'og:title'}, None),
        ({'property': 'og:title', 'content': 'title'}, 'title'), ],
    ids=[
        'empty',
        'not-set',
        'title', ])
def test_get_og_title(tag, expected):
    received = get_og_title(tag)

    assert received == expected


@mark.parametrize('name', BASIC_INTERMED)
def test_get_title(name: str):
    expected = '{} Title'.format(name.title())

    src = get_soup(name)
    received = get_title(src)

    assert received == expected


class TestHtmlDocument(TestTextDocument):
    @param_document_init(HtmlDocument, 'html', ['basic', 'intermed'])
    def test___init__(self, inst: HtmlDocument, expected: DOC_INIT_EXPECTED):
        assert self.compare_document(inst, expected)

    @param_supports('htm', 'html')
    def test_supports(self, path, ext, expected):
        expected = expected or path.startswith('http')
        received = HtmlDocument.supports(path, ext)

        assert received == expected or 'supports' == 0
