""" Simple I/O module tests """

from pathlib import Path

from oolongt import parser, simple_io

from .helpers import assert_ex


def get_json_path(lang):
    # type: (str) -> str
    """Get path to test language config

    Arguments:
        lang {str} -- language

    Returns:
        str -- path to language config JSON file
    """
    return Path(__file__).parent.joinpath(
        'lang', lang + parser.JSON_SUFFIX)


def test_load_json():
    """Test correct JSON parse"""
    path = get_json_path('valid')

    expected = {
        'meta': {
            'name': 'Valid Language Config'
        },
        'ideal': 2,
        'nltk_language': 'valid',
        'stop_words': ['foo', 'bar']}
    received = simple_io.load_json(path)

    assert (received == expected), assert_ex(
        'json data', repr(received), repr(expected))


def test_read_file():
    """Test correct file read"""
    path = get_json_path('malformed')

    expected = '{\n'
    received = simple_io.read_file(path)

    assert (received == expected), assert_ex(
        'read file', repr(received), repr(expected))
