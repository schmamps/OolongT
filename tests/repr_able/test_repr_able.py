"""Test ReprAble"""
from pytest import mark

from src.oolongt.repr_able import ReprAble
from tests.helpers import pad_to_longest


# pylint: disable=no-self-use,too-few-public-methods,protected-access
class TestReprAble:
    """Test ReprAble"""
    @mark.parametrize(
        'args,kwargs,expected',
        [
            ([], {}, 'ReprAble()'),
            (['one', 'two'], {}, 'ReprAble(\'one\', \'two\')'),
            ([], {'one': 1, 'two': 2}, 'ReprAble(one=1, two=2)'),
            (['one'], {'two': 2}, 'ReprAble(\'one\', two=2)'), ],
        ids=pad_to_longest(['empty', 'args', 'kwargs', 'both']))
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
