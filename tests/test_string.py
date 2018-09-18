"""Test string module"""
import typing

from src.oolongt import it
from src.oolongt.string import (
    AnyOrAnys, cast, define_join, define_split, filter_empty, simplify, split,
    strip)
from src.oolongt.typings import StringList
from tests.params.string import (
    param_cast, param_define_split_join, param_filter_empty, param_simplify,
    param_split, param_strip)


@param_cast()
def test_cast(val: AnyOrAnys, expected: StringList):
    """Test `cast` in string module

    Arguments:
        val {AnyOrAnys} -- value or values
        expected {StringList} -- expected result
    """
    received = cast(val)

    if it.erable(expected):
        received = list(received)

    assert received == expected


def _test_split_join(
        func: typing.Callable,
        sep: str,
        arg: typing.Any,
        expected: typing.Any):
    """Test split and join functions

    Arguments:
        func {typing.Callable} -- split/join function
        sep {str} -- separator to intiialize function
        arg {typing.Any} -- argument passed to initialized function
        expected {typing.Any} -- expected result
    """
    call = func(sep)
    received = call(arg)

    assert received == expected


@param_define_split_join()
def test_define_split(sep: str, str_val: str, list_val: StringList):
    """Test `define_split` in string module

    Arguments:
        sep {str} -- separator to initialze function
        str_val {str} -- string to split
        list_val {StringList} -- expected result
    """
    _test_split_join(define_split, sep, str_val, list_val)


@param_define_split_join()
def test_define_join(sep: str, str_val: str, list_val: StringList):
    """Test `define_join` in string module

    Arguments:
        sep {str} -- separator to initialize function
        str_val {str} -- expected result
        list_val {StringList} -- list of strings to join
    """
    _test_split_join(define_join, sep, list_val, str_val)


@param_strip()
def test_strip(val: StringList, expected: StringList):
    """Test `strip` in string module

    Arguments:
        val {StringList} -- string or strings to strip
        expected {StringList} -- expected result
    """
    received = strip(val)

    if it.erable(expected):
        assert list(received) == list(expected)

    else:
        assert received == expected


@param_filter_empty()
def test_filter_empty(val: StringList, expected: StringList):
    """Test `filter_empty` in string module

    Arguments:
        val {StringList} -- list of strings
        expected {StringList} -- expected result
    """
    received = list(filter_empty(val))

    assert received == expected


@param_split()
def test_split(val: typing.Any, kwargs: dict, expected: StringList):
    """Test `split` in string module

    Arguments:
        val {typing.Any} -- input value
        kwargs {dict} -- arguments passed to `split`
        expected {StringList} -- expected result
    """
    received = list(split(val, **kwargs))

    assert received == expected


def test_norm_nfkd():
    """Ignore non-novel code in `norm_nfkd`"""
    pass


def test_encode_ascii():
    """Ignore non-novel code in `encode_ascii`"""
    pass


def test_decode_utf8():
    """Ignore non-novel code in `decode_utf8`"""
    pass


@param_simplify()
def test_simplify(val: typing.Any, expected: str):
    """Test `simplify` in string module"""
    received = simplify(val)

    assert received == expected
