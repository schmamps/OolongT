"""Parametrize I/O tests"""
import typing
from json import JSONDecodeError

from pytest import mark

from tests.constants import DOC_PATH, IDIOM_PATH
from tests.helpers import pad_to_longest

from .content import get_doc_path


def param_read(on_dir=OSError, on_404=OSError):
    """Parametrize read tests

    Keyword Arguments:
        on_dir {Exception} -- expected error on directory (default: {OSError})
        on_404 {Exception} -- expected error on not found (default: {OSError})
    """
    return mark.parametrize(
        'path,expected',
        [
            (get_doc_path('basic', 'txt'), 'Basic body'),
            (str(DOC_PATH), on_dir),
            (get_doc_path('basic', 'webm'), on_404)],
        ids=pad_to_longest(['basic', 'dir', 'error']))


def param_json(filename: typing.AnyStr, success: bool):
    """Parametrize JSON test

    Arguments:
        filename {str} -- path to document
        success {bool} -- success is expected
    """
    expected = JSONDecodeError  # type: typing.Any

    if success:
        expected = {
            'meta': {
                'name': 'Valid Language Config'
            },
            'ideal': 2,
            'language': 'valid',
            'stop_words': {'nltk': False, 'user': ['spam', 'eggs']}}

    return (str(IDIOM_PATH.joinpath(filename)), expected)
