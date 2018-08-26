""" Simple I/O module tests """
import typing
from pathlib import Path

from pytest import mark

from src.oolongt import simple_io
from tests.constants import IDIOM_PATH
from tests.helpers import assert_ex


def get_json_path(idiom: str) -> Path:
    """Get path to test idiom config

    Arguments:
        idiom {str} -- idiom

    Returns:
        str -- path to idiom config JSON file
    """
    return IDIOM_PATH.joinpath(idiom + '.json')


@mark.parametrize(
    'path',
    [(get_json_path('valid'))],
    ids=['valid'])
def test_load_json(path: typing.Any) -> None:
    """Test correct JSON parse"""
    expected = {
        'meta': {
            'name': 'Valid Language Config'
        },
        'ideal': 2,
        'language': 'valid',
        'stop_words': {'nltk': False, 'user': ['foo', 'bar']}}
    received = simple_io.load_json(path)

    assert (received == expected), assert_ex(
        'json data',
        repr(received),
        repr(expected))


@mark.parametrize(
    'path',
    [(get_json_path('malformed'))],
    ids=['malformed'])
def test_read_file(path: typing.Any) -> None:
    """Test correct file read"""
    expected = '{\n'
    received = simple_io.read_file(path)

    assert (received == expected), assert_ex(
        'read file',
        repr(received),
        repr(expected))
