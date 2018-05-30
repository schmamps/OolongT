from textteaser import nodash

from .assert_ex import assert_ex

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
    result = nodash.pluck(VALID_DICT_LIST, TEST_KEY)

    assert_ex('pluck', result, expected)


def test_pluck_invalid():
    expected = True

    try:
        result = nodash.pluck(INVALID_DICT_LIST, TEST_KEY)

    except KeyError:
        result = expected

    test = (result == expected)

    assert_ex('pluck error check', result, KeyError, test=test)


def test_sort_by_valid_asc():
    expected = VALID_DICT_LIST_SORTED
    result = nodash.sort_by(VALID_DICT_LIST, TEST_KEY)

    assert_ex('sort by key asc', result, expected, hint=TEST_KEY)


def test_sort_by_valid_desc():
    expected = list(reversed(VALID_DICT_LIST_SORTED))
    result = nodash.sort_by(VALID_DICT_LIST, TEST_KEY, reverse=True)

    assert_ex('sort by key desc', result, expected, hint=TEST_KEY)


def test_sort_by_invalid():
    expected = True
    invalid = 'y'

    try:
        result = nodash.sort_by(INVALID_DICT_LIST, invalid)

    except KeyError:
        result = expected

    test = (result == expected)

    assert_ex('sort error check', result, KeyError, test=test, hint=invalid)
