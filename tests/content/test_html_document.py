"""Test HtmlDocument content class"""
from pytest import mark

from src.oolongt.content import HtmlDocument
from src.oolongt.content.content import norm_text
from src.oolongt.content.html_document import (
    get_body, get_og_title, get_source, get_title, process)
from src.oolongt.io import read_file
from src.oolongt.ugly_soup import UglySoup
from test_text_document import TestTextDocument
from tests.helpers import pad_to_longest
from tests.params.content import (
    DocumentInit, compare_document, get_doc_path, param_document_init,
    param_supports)

STEMS = ['basic', 'intermed']
EXTENSION = 'html'
BASIC_INTERMED = STEMS


def get_path(stem: str) -> str:
    """Get path to sample named `stem`

    Arguments:
        stem {str} -- stem of sample path

    Returns:
        str -- full path to sample
    """
    return get_doc_path(stem, 'html')


def get_html(stem: str) -> str:
    """Get HTML of sample named `stem`

    Arguments:
        stem {str} -- stem of sample path

    Returns:
        str -- HTML of file
    """
    path = get_path(stem)

    return read_file(path)


def get_soup(stem: str) -> UglySoup:
    """Parse HTML from sample named `stem`

    Arguments:
        stem {str} -- stem of sample path

    Returns:
        UglySoup -- HTML, parsed
    """
    html = get_html(stem)

    return UglySoup(html)


@mark.parametrize('stem', BASIC_INTERMED)
def test_process(stem: str):
    """Verify that HTML can be processed

    Arguments:
        stem {str} -- stem of sample path
    """
    expected = UglySoup

    html = get_html(stem)
    received = process(html)

    assert isinstance(received, expected)


@mark.parametrize('stem', BASIC_INTERMED)
def test_get_source(stem: str):
    """Test get_source

    Arguments:
        stem {str} -- stem of sample path
    """
    expected = False

    path = get_path(stem)
    soup = get_source(path)
    received = '<script' in soup.prettify()

    assert received == expected


@mark.parametrize('stem', BASIC_INTERMED)
def test_get_body(stem: str):
    """Verify body of sample named `stem`

    Arguments:
        stem {str} -- stem of sample path
    """
    expected = '{} body'.format(stem.title())

    src = get_soup(stem)
    received = norm_text(get_body(src))

    assert received == expected


@mark.parametrize(
    'tag,expected',
    [
        ({}, None),
        ({'property': 'og:title'}, None),
        ({'property': 'og:title', 'content': 'title'}, 'title'), ],
    ids=pad_to_longest([
        'empty',
        'not-set',
        'title', ]))
def test_get_og_title(tag, expected):
    """Test OpenGraph title

    Arguments:
        tag {dict} -- dictionary of values
        expected {OptionalString} -- expected value
    """
    received = get_og_title(tag)

    assert received == expected


@mark.parametrize('stem', BASIC_INTERMED)
def test_get_title(stem: str):
    """Test <title> tag

    Arguments:
        stem {str} -- stem of sample path
    """
    expected = '{} Title'.format(stem.title())

    src = get_soup(stem)
    received = get_title(src)

    assert received == expected


class TestHtmlDocument(TestTextDocument):
    """Test HtmlDocument subclass"""
    @param_document_init(HtmlDocument, EXTENSION, STEMS)
    def test___init__(self, inst: HtmlDocument, expected: DocumentInit):
        assert compare_document(inst, expected)

    @param_supports('htm', EXTENSION)
    def test_supports(self, path, ext, expected):
        expected = expected or path.startswith('http')

        assert self.supports(HtmlDocument, path, ext, expected)

    @param_document_init(HtmlDocument, EXTENSION, STEMS)
    def test___repr__(self, inst, expected):
        assert self._test_doc_repr(inst, expected)
