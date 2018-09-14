"""Parametrize I/O tests"""
import typing
from json import JSONDecodeError
from pathlib import Path

from tests.constants import DOC_PATH, IDIOM_PATH
from tests.params.helpers import parametrize

from .content import get_doc_path


def param_scheme():
    """Parametrize `test_is_supported_scheme`"""
    names = 'path,expected'
    vals = (
        ('/etc/hosts', False),
        ('file:///etc/hosts', True),
        ('ftp://x', True),
        ('http://x', True),
        ('https://x', True),
    )
    ids = (
        'local',
        'file:',
        'ftp:',
        'http:',
        'https:',
    )

    return parametrize(names, vals, ids)


def param_get_absolute_path():
    """Parametrize `test_get_absolute_path`"""
    abs_file = str(Path(__file__).absolute())

    names = 'path,expected'
    vals = ((__file__, abs_file), (Path(__file__), abs_file), )
    ids = ('str', 'Path', )

    return parametrize(names, vals, ids)


def param_get_local_url():
    """Parametrize `test_get_local_url`"""
    names = 'path,expected'
    vals = (('/spam/eggs/bacon.ham', 'file:///spam/eggs/bacon.ham'), )
    ids = ('spam', )

    return parametrize(names, vals, ids)


def param_read(on_dir=OSError, on_404=OSError):
    """Parametrize read tests

    Keyword Arguments:
        on_dir {Exception} -- expected error on directory (default: {OSError})
        on_404 {Exception} -- expected error on not found (default: {OSError})
    """
    names = 'path,expected'
    vals = (
        (get_doc_path('basic', 'txt'), 'Basic body'),
        (str(DOC_PATH), on_dir),
        (get_doc_path('basic', 'webm'), on_404),
    )
    ids = ('basic', 'dir', 'error', )

    return parametrize(names, vals, ids)


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
            'stop_words': {'nltk': False, 'user': ['spam', 'eggs']}
        }

    return (str(IDIOM_PATH.joinpath(filename)), expected, )


def param_load_json():
    """Parametrize `test_load_json`"""
    names = 'path,expected'
    vals = [
        param_json('valid.json', True),
        param_json('valid.FAIL', False),
        param_json('malformed.json', False),
    ]
    ids = ('valid', 'bad_path', 'malformed', )

    return parametrize(names, vals, ids)
