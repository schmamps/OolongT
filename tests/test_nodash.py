""" Test lodash-like functionality """
from pytest import mark

from oolongt.nodash import pluck, sort_by

from .helpers import assert_ex, check_exception

TEST_KEY = 'test_key'
VALID_DICT_LIST = [
    {TEST_KEY: 3},
    {'y': 2, TEST_KEY: 1},
    {'z': 3, 'y': 1, TEST_KEY: 2}]

INVALID_DICT_LIST = [
    {TEST_KEY: 1},
    {'y': 1, TEST_KEY: 2},
    {'z': 1, 'y': 2}]
VALID_DICT_LIST_SORTED = [
    {'y': 2, TEST_KEY: 1},
    {'z': 3, 'y': 1, TEST_KEY: 2},
    {TEST_KEY: 3}]
VALID_DICT_LIST_REVERSED = list(reversed(VALID_DICT_LIST_SORTED))
REV_KWARG = {'reverse': True}


@mark.parametrize('data,expected', [
    (VALID_DICT_LIST, [3, 1, 2]),
    (INVALID_DICT_LIST, KeyError),
])
def test_pluck(data, expected):
    received = None

    try:
        received = pluck(data, TEST_KEY)

    except KeyError as e:
        received = check_exception(e, expected)

    assert (received == expected), assert_ex(
        'pluck', received, expected)


@mark.parametrize('data,expected,kwargs,key', [
    (VALID_DICT_LIST, VALID_DICT_LIST_SORTED, False, False),
    (VALID_DICT_LIST, VALID_DICT_LIST_REVERSED, REV_KWARG, False),
    (INVALID_DICT_LIST, KeyError, False, 'y')
])
def test_sort_by(data, expected, kwargs, key):
    kwargs = kwargs or {}
    key = key or TEST_KEY
    received = None

    try:
        received = sort_by(data, key, **kwargs)

    except KeyError as e:
        received = check_exception(e, expected)

    assert (received == expected), assert_ex(
        'sort by key', received, expected, hint=[key, kwargs])
