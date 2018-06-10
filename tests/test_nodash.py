from oolongt import nodash

from .helpers import assert_ex

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


def test_pluck_valid():
    expected = [3, 1, 2]
    received = nodash.pluck(VALID_DICT_LIST, TEST_KEY)

    assert (received == expected), assert_ex(
        'pluck', received, expected)


def test_pluck_invalid():
    expected = True

    try:
        received = nodash.pluck(INVALID_DICT_LIST, TEST_KEY)

    except KeyError:
        received = expected

    assert (received == expected), assert_ex(
        'pluck error check', received, KeyError)


def test_sort_by_valid_asc():
    expected = VALID_DICT_LIST_SORTED
    received = nodash.sort_by(VALID_DICT_LIST, TEST_KEY)

    assert (received == expected), assert_ex(
        'sort by key asc', received, expected, hint=TEST_KEY)


def test_sort_by_valid_desc():
    expected = list(reversed(VALID_DICT_LIST_SORTED))
    received = nodash.sort_by(VALID_DICT_LIST, TEST_KEY, reverse=True)

    assert (received == expected), assert_ex(
        'sort by key desc', received, expected, hint=TEST_KEY)


def test_sort_by_invalid():
    expected = True
    invalid = 'y'

    try:
        received = nodash.sort_by(INVALID_DICT_LIST, invalid)

    except KeyError:
        received = expected

    assert (received == expected), assert_ex(
        'sort error check', received, KeyError, hint=invalid)
