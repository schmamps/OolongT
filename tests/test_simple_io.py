""" Simple I/O module tests """
from pathlib import Path

from pytest import mark

from oolongt import parser, simple_io

from tests.helpers import assert_ex


def get_json_path(lang):
    # type: (str) -> str
    """Get path to test language config

    Arguments:
        lang {str} -- language

    Returns:
        str -- path to language config JSON file
    """
    return Path(__file__).parent.joinpath(
        'lang', lang + '.json')


@mark.parametrize(
    'path',
    [(get_json_path('valid'))],
    ids=['valid'])
def test_load_json(path):
    """Test correct JSON parse"""
    expected = {
        'meta': {
            'name': 'Valid Language Config'
        },
        'ideal': 2,
        'nltk_language': 'valid',
        'stop_words': {'initial': [], 'custom': ['foo', 'bar']}}
    received = simple_io.load_json(path)

    assert (received == expected), assert_ex(
        'json data', repr(received), repr(expected))


@mark.parametrize(
    'path',
    [(get_json_path('malformed'))],
    ids=['malformed'])
def test_read_file(path):
    """Test correct file read"""
    expected = '{\n'
    received = simple_io.read_file(path)

    assert (received == expected), assert_ex(
        'read file', repr(received), repr(expected))
