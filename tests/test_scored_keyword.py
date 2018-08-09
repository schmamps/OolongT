import typing

from pytest import mark

from oolongt.typedefs.scored_keyword import (KEYWORD_SCORE_K, ScoredKeyword,
                                             compare_keywords, compare_length,
                                             compare_score, compare_word,
                                             score_keyword)
from tests.helpers import assert_ex, check_exception, index_of, pad_to_longest


def hint_keyword(keyword: ScoredKeyword) -> str:
    """Cast `ScoredKeyword` to lightly-detailed string

    Arguments:
        keyword {ScoredKeyword} -- keyword

    Returns:
        str -- word and score
    """
    return '{!r}: {}'.format(keyword.word, keyword.score)


def hint_keywords(*args: ScoredKeyword) -> str:
    """Cast list of `ScoredKeyword`s as lightly-detailed strings

    Returns:
        str -- keyword details
    """
    return '/'.join([hint_keyword(x) for x in args])


def set_test(
        a_params: typing.Tuple[str, int, int],
        b_params: typing.Tuple[str, int, int],
        *args: typing.Any
        ) -> typing.Tuple:
    word_a, count_a, of_a = a_params
    word_b, count_b, of_b = b_params

    items = [
        ScoredKeyword(word_a, count_a, of_a),
        ScoredKeyword(word_b, count_b, of_b), ]

    items += args

    return tuple(items)


def get_value_tests() -> typing.List[typing.Tuple]:
    """Get tests for comparing ScoredKeyword values

    Returns:
        typing.List[typing.Tuple] --
            [0]: `a: ScoredKeyword`
            [1]: `b: ScoredKeyword`
            [2]: `a lt b`
            [3]: `a == b`
    """
    return [
        set_test(('foo', 1, 1), ('foo', 1, 1), False, True),
        set_test(('foo', 1, 1), ('foo', 2, 2), False, True),
        set_test(('foo', 1, 2), ('foo', 1, 1), True, False),
        set_test(('foo', 1, 1), ('foo', 1, 2), False, False),
        set_test(('foo', 1, 1), ('foobar', 1, 1), True, False),
        set_test(('foobar', 1, 1), ('foo', 1, 1), False, False),
    ]


def get_value_ids() -> typing.List[str]:
    """Get IDs for `get_value_tests()`

    Returns:
        typing.List[str] -- test IDS
    """
    return [
        '(word: a=b, count: a=b, of: a=b, score: a=b) == eq',
        '(word: a=b, count: a<b, of: a<b, score: a=b) == eq',
        '(word: a=b, count: a=b, of: a>b, score: a=b) == lt',
        '(word: a=b, count: a=b, of: a<b, score: a=b) == gt',
        '(word: a<b, count: a=b, of: a=b, score: a=b) == lt',
        '(word: a>b, count: a=b, of: a=b, score: a=b) == gt',
    ]


@mark.parametrize(
    'count,of,expected',
    [
        (1, 1, 1.5),
        (1, 2, .75),
        (1, 10, .15),
        (1, 0, ValueError),
    ],
    ids=[
        '1 of    1',
        '1 of    2',
        '1 of   10',
        '1 of 0(!)',
    ])
def test_score_keyword(count: int, of: int, expected: float) -> None:
    try:
        received = score_keyword(count, of)

    except ValueError as e:
        received = check_exception(e, expected)

    assert (received == expected), assert_ex(
        'score keyword',
        received,
        expected,
        hint=index_of(count, of))


@mark.parametrize(
    'a,b,expected',
    [
        set_test(('foo', 1, 1), ('foo', 1, 1), 0),
        set_test(('foo', 1, 1), ('bar', 1, 1), 0),
        set_test(('foo', 1, 2), ('foo', 1, 1), -1),
        set_test(('foo', 1, 2), ('bar', 1, 1), -1),
        set_test(('foo', 1, 1), ('foo', 1, 2), 1),
        set_test(('foo', 1, 1), ('bar', 1, 2), 1),
    ],
    ids=[
        '(word: eq, score: a=b) == 0',
        '(word: ne, score: a=b) == 0',
        '(word: eq, score: a<b) == -',
        '(word: ne, score: a<b) == -',
        '(word: eq, score: a>b) == +',
        '(word: ne, score: a>b) == +',
    ])
def test_compare_score(
        a: ScoredKeyword,
        b: ScoredKeyword,
        expected: int
        ) -> None:
    received = compare_score(a, b)

    assert (received == expected), assert_ex(
        'compare keyword score',
        received,
        expected,
        hint=hint_keywords(a, b))


@mark.parametrize(
    'a,b,expected',
    [
        set_test(('foo', 1, 1), ('foo', 1, 1), 0),
        set_test(('foo', 1, 1), ('bar', 1, 1), 0),
        set_test(('foo', 1, 1), ('quux', 1, 1), -1),
        set_test(('quux', 1, 1), ('foo', 1, 1), 1),
    ], ids=[
        '(word: eq, len: a=b) == 0',
        '(word: ne, len: a=b) == 0',
        '(word: ne, len: a<b) == -',
        '(word: ne, len: a>b) == +',
    ])
def test_compare_length(
        a: ScoredKeyword,
        b: ScoredKeyword,
        expected: int
        ) -> None:
    received = compare_length(a, b)

    assert (received == expected), assert_ex(
        'compare keyword length',
        received,
        expected,
        hint=hint_keywords(a, b))


@mark.parametrize(
    'a,b,expected',
    [
        set_test(('foo', 1, 1), ('foo', 1, 1), 0),
        set_test(('foo', 1, 1), ('bar', 1, 1), 1),
        set_test(('foo', 1, 1), ('qux', 1, 1), -1),
    ],
    ids=[
        '(a eq b) == 0',
        '(a gt b) == +',
        '(a lt b) == -',
    ])
def test_compare_word(
        a: ScoredKeyword,
        b: ScoredKeyword,
        expected: int
        ) -> None:
    received = compare_word(a, b)

    assert (received == expected), assert_ex(
        'compare keyword word',
        received,
        expected,
        hint=hint_keywords(a, b))


# trip all factors (individual factors tested separately)
@mark.parametrize(
    'a,b,expected',
    [
        set_test(('foo', 1, 2), ('quux', 1, 1), (-1, -1, -1)),
        set_test(('foo', 1, 1), ('foo', 1, 1), (0, 0, 0)),
        set_test(('foo', 1, 1), ('ba', 1, 2), (1, 1, 1)),
    ],
    ids=[
        '(score: a<b, len: a<b, str: a<b)[:] == (-) * 3',
        '(score: a=b, len: a=b, str: a=b)[:] == (0) * 3',
        '(score: a>b, len: a>b, str: a>b)[:] == (+) * 3',
    ])
def test_compare_keywords(
        a: ScoredKeyword,
        b: ScoredKeyword,
        expected: typing.Tuple[int, int, int]
        ) -> None:
    received = compare_keywords(a, b)

    assert (received == expected), assert_ex(
        'compare keywords',
        received,
        expected,
        hint=hint_keywords(a, b))


class TestScoredKeyword:
    @mark.parametrize(
        'keyword,_,expected',
        [
            set_test(('foo', 1, 1), ('', 1, 1), 'foo'),
            set_test(('bar', 1, 1), ('', 1, 1), 'bar'),
            set_test(('Validation? No!', 1, 1), ('', 1, 1), 'validation? no!'),
        ],
        ids=pad_to_longest([
            'foo',
            'bar',
            'unvalidated',
        ]))
    def test_str(
            self,
            keyword: ScoredKeyword,
            _: ScoredKeyword,
            expected: str
            ) -> None:
        received = str(keyword)

        assert (received == expected), assert_ex(
            'keyword string cast',
            received,
            expected,
            hint=keyword)

    @mark.parametrize(
        'a,b,_,expected',
        get_value_tests(),
        ids=get_value_ids())
    def test_eq(
            self,
            a: ScoredKeyword,
            b: ScoredKeyword,
            _: bool,
            expected: bool
            ) -> None:
        received = (a == b)

        assert (received == expected), assert_ex(
            'keyword equality',
            received,
            expected,
            hint=hint_keywords(a, b))

    @mark.parametrize(
        'a,b,expected,_',
        get_value_tests(),
        ids=get_value_ids())
    def test_lt(
            self,
            a: ScoredKeyword,
            b: ScoredKeyword,
            expected: bool,
            _: bool
            ) -> None:
        received = (a < b)

        assert (received == expected), assert_ex(
            'keyword lt',
            received,
            expected,
            hint=hint_keywords(a, b))

    @mark.parametrize(
        'a,b,lt,eq',
        get_value_tests(),
        ids=get_value_ids())
    def test_gt(
            self,
            a: ScoredKeyword,
            b: ScoredKeyword,
            lt: bool,
            eq: bool
            ) -> None:
        expected = not (lt or eq)
        received = (a > b)

        assert (received == expected), assert_ex(
            'keyword gt',
            received,
            expected,
            hint=hint_keywords(a, b))
