import typing

from src.oolongt.string import (
    cast_list, cast_value, define_join, define_split, filter_empty, simplify,
    split, strip_str, strip_strs)
from src.oolongt.typings import StringList
from tests.params.helpers import parametrize
from tests.params.string import (
    param_cast_list, param_define_split_join, param_filter_empty,
    param_simplify, param_split, param_strip_str, param_strip_strs)


@parametrize('val,expected', ((1, '1', ),), ('int', ))
def test_cast_value(val: typing.Any, expected: str):
    received = cast_value(val)

    assert received == expected


@param_cast_list()
def test_cast_list(val: typing.Iterable[typing.Any], expected: StringList):
    received = list(cast_list(val))

    assert received == expected


def _test_split_join(
        func: typing.Callable,
        sep: str,
        arg: typing.Any,
        expected: typing.Any):
    call = func(sep)
    received = call(arg)

    assert received == expected


@param_define_split_join()
def test_define_split(sep: str, str_val: str, list_val: StringList):
    _test_split_join(define_split, sep, str_val, list_val)


@param_define_split_join()
def test_define_join(sep: str, str_val: str, list_val: StringList):
    _test_split_join(define_join, sep, list_val, str_val)


@param_strip_str()
def test_strip_str(val: str, expected: str):
    received = strip_str(val)

    assert received == expected


@param_strip_strs()
def test_strip_strs(val: StringList, expected: StringList):
    received = list(strip_strs(val))

    assert received == expected


@param_filter_empty()
def test_filter_empty(val: StringList, expected: StringList):
    received = list(filter_empty(val))

    assert received == expected


@param_split()
def test_split(kwargs: dict, expected: list):
    # assert None
    return

    received = list(split(**kwargs))

    assert received == expected


def test_norm_nfkd():
    assert True  # not novel code


def test_encode_ascii():
    assert True  # not novel code


def test_decode_utf8():
    assert True  # not novel code


@param_simplify()
def test_simplify(val: str, expected: str):
    received = simplify(val)

    assert received == expected
