import pytest

from oolongt.typing.scored_keyword import (
    score_keyword,
    compare_length, compare_score, compare_word, compare_keywords,
    KEYWORD_SCORE_K, ScoredKeyword)
from tests.helpers import assert_ex, check_exception


def set_test(a_params, b_params, *args):
    # type: (tuple[str, int, int], tuple[str, int, int], any)
    word_a, count_a, of_a = a_params
    word_b, count_b, of_b = b_params

    items = [
        ScoredKeyword(word_a, count_a, of_a),
        ScoredKeyword(word_b, count_b, of_b), ]

    items += args

    return tuple(items)


def get_value_tests():
    return [
        set_test(('foo', 1, 1), ('foo', 1, 1), False, True),
        set_test(('foo', 1, 1), ('foo', 2, 2), False, True),
        set_test(('foo', 1, 1), ('foobar', 1, 1), True, False),
        set_test(('foo', 1, 1), ('bar', 1, 1), False, False),
        set_test(('foo', 1, 2), ('foo', 1, 1), True, False),
        set_test(('foo', 1, 1), ('foo', 1, 2), False, False), ]


@pytest.mark.parametrize('count,of,expected', [
    (1, 1, 1.5),
    (1, 2, .75),
    (1, 10, .15),
    (1, 0, ValueError),
])
def test_score_keyword(count, of, expected):
    # type: (int, int, any) -> None
    try:
        received = score_keyword(count, of)

    except ValueError as e:
        received = check_exception(e, expected)

    assert (received == expected), assert_ex(
        'score keyword',
        received,
        expected,
        hint=' of '.join([count, of]))


@pytest.mark.parametrize('a,b,expected', [
    set_test(('foo', 1, 1), ('foo', 1, 1), 0),
    set_test(('foo', 1, 1), ('bar', 1, 1), 0),
    set_test(('foo', 1, 1), ('foo', 1, 2), 1),
    set_test(('foo', 1, 2), ('foo', 1, 1), -1),
])
def test_compare_score(a, b, expected):
    received = compare_score(a, b)

    assert (received == expected), assert_ex(
        'compare keyword score',
        received,
        expected,
        hint=[a, b])


@pytest.mark.parametrize('a,b,expected', [
    set_test(('foo', 1, 1), ('foo', 1, 1), 0),
    set_test(('foo', 1, 1), ('bar', 1, 1), 0),
    set_test(('foo', 1, 1), ('fo', 1, 1), 1),
    set_test(('foo', 1, 1), ('quux', 1, 1), -1),
])
def test_compare_length(a, b, expected):
    received = compare_length(a, b)

    assert (received == expected), assert_ex(
        'compare keyword length',
        received,
        expected,
        hint=[a, b])


@pytest.mark.parametrize('a,b,expected', [
    set_test(('foo', 1, 1), ('foo', 1, 1), 0),
    set_test(('foo', 1, 1), ('bar', 1, 1), 1),
    set_test(('foo', 1, 1), ('qux', 1, 1), -1),
])
def test_compare_word(a, b, expected):
    received = compare_word(a, b)

    assert (received == expected), assert_ex(
        'compare keyword word',
        received,
        expected,
        hint=[a, b])


@pytest.mark.parametrize('a,b,expected', [
    set_test(('foo', 1, 1), ('foo', 1, 1), (0, 0, 0)),
    set_test(('foo', 1, 1), ('foo', 1, 2), (1, 0, 0)),
    set_test(('foo', 1, 1), ('quux', 1, 1), (0, -1, -1)),
    set_test(('foo', 1, 1), ('fo', 1, 1), (0, 1, 1)),
    set_test(('foo', 1, 1), ('bar', 1, 1), (0, 0, 1)),
    set_test(('foo', 1, 1), ('qux', 1, 1), (0, 0, -1)),
    set_test(('foo', 1, 1), ('ba', 1, 2), (1, 1, 1)),
    set_test(('foo', 1, 2), ('quux', 1, 1), (-1, -1, -1)),
])
def test_compare_keywords(a, b, expected):
    received = compare_keywords(a, b)

    assert (received == expected), assert_ex(
        'compare keywords',
        received,
        expected,
        hint=[a, b])


class TestScoredKeyword:
    @pytest.mark.parametrize('keyword,_,expected', [
        set_test(('foo', 1, 1), ('', 1, 1), 'foo'),
        set_test(('bar', 1, 1), ('', 1, 1), 'bar'),
        set_test(('Validation? No!', 1, 1), ('', 1, 1), 'validation? no!'),
    ])
    def test_str(self, keyword, _, expected):
        received = str(keyword)

        assert (received == expected), assert_ex(
            'keyword to string',
            received,
            expected,
            hint=keyword)

    @pytest.mark.parametrize('a,b,_,expected', get_value_tests())
    def test_eq(self, a, b, _, expected):
        received = (a == b)

        assert (received == expected), assert_ex(
            'keyword equality',
            received,
            expected,
            hint=[a, b]
        )

    @pytest.mark.parametrize('a,b,expected,_', get_value_tests())
    def test_lt(self, a, b, expected, _):
        received = (a < b)

        assert (received == expected), assert_ex(
            'keyword equality',
            received,
            expected,
            hint=[a, b]
        )

    @pytest.mark.parametrize('a,b,lt,eq', get_value_tests())
    def test_gt(self, a, b, lt, eq):
        expected = not (lt or eq)
        received = (a > b)

        assert (received == expected), assert_ex(
            'keyword equality',
            received,
            expected,
            hint=[a, b]
        )
