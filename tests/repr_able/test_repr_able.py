"""Test ReprAble"""
from src.oolongt.repr_able import ReprAble
from tests.params.repr_able import param_repr


# pylint: disable=no-self-use,too-few-public-methods,protected-access
class TestReprAble:
    """Test ReprAble"""
    @param_repr()
    def test__repr_(self, args: list, kwargs: dict, expected: str):
        """Test `ReprAble._repr_`

        Arguments:
            args {list} -- positional arguments
            kwargs {dict} -- keyword arguments
            expected {str} -- expected REPR
        """
        inst = ReprAble()
        received = inst._repr_(*args, **kwargs)

        assert received == expected
