"""Test pipe subpackage"""
import typing

from src.oolongt.pipe import noop, pipe
from tests.params.pipe import param_noop, param_pipe


@param_noop()
def test_noop(expected: typing.Any):
    """Test `noop`

    Arguments:
        expected {typing.Any} -- expected value (same as input)
    """
    received = noop(expected)

    assert received == expected


@param_pipe()
def test_pipe(
        init: typing.Any,
        pipeline: typing.Any,
        expected: typing.Any):
    """Test `pipe`

    Arguments:
        init {typing.Any} -- input value
        pipeline {typing.Any} -- (iterable of) callables
        expected {typing.Any} -- expected result
    """
    received = pipe(init, pipeline)

    assert received == expected
