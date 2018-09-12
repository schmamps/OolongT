"""Test pipelining"""
import typing
from pytest import mark

from src.oolongt.pipe import noop, pipe
from tests.helpers import pad_to_longest, return_false, return_true


@mark.parametrize(
    'expected',
    [(''), (0), (True), (False), (None)],
    ids=pad_to_longest(['empty', 'zero', 'true', 'false', 'none']))
def test_noop(expected: typing.Any):
    """Test noop

    Arguments:
        expected {typing.Any} -- expected value (same as input)
    """
    received = noop(expected)

    assert received == expected


@mark.parametrize(
    'init,pipeline,expected',
    [
        (0, return_false, False),
        (0, (return_false, return_true), True),
        (0, (noop, (noop, noop), [noop, noop]), 0)],
    ids=pad_to_longest(['simple', 'tuple', 'complex']))
def test_pipe(
        init: typing.Any,
        pipeline: typing.Any,
        expected: typing.Any):
    """Test pipe

    Arguments:
        init {typing.Any} -- input value
        pipeline {typing.Iterable} -- list of callables
        expected {typing.Any} -- expected result
    """
    received = pipe(init, pipeline)

    assert received == expected
