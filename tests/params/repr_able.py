"""Test ReprAble params"""
from tests.params.helpers import parametrize


def param_repr():
    """Parametrize `test__repr_`"""
    names = 'args,kwargs,expected'
    vals = (
        ([], {}, 'ReprAble()'),
        (['one', 'two'], {}, 'ReprAble(\'one\', \'two\')'),
        ([], {'one': 1, 'two': 2}, 'ReprAble(one=1, two=2)'),
        (['one'], {'two': 2}, 'ReprAble(\'one\', two=2)'),
    )
    ids = ('empty', 'args', 'kwargs', 'both')

    return parametrize(names, vals, ids)
