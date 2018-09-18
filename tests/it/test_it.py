"""Test it subpackage"""
import typing

from src.oolongt import it
from tests.params.it import param_it_erable, param_it_erate


@param_it_erable()
def test_it_erable(val: typing.Any, expected: bool):
    """Test `it.erable`

    Arguments:
        val {typing.Any} -- any value
        expected {bool} -- value is iterable (but not str)
    """
    received = it.erable(val)

    assert received == expected


@param_it_erate()
def test_it_erate(val: typing.Any):
    """Test `it.erate`

    Arguments:
        val {typing.Any} -- any value
    """
    received = it.erate(val)

    assert it.erable(received)
