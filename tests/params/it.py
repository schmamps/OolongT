"""Test parameters for it subpackage"""
from .helpers import parametrize


def param_it_erable():
    """Parametrize `test_it_erable`"""
    names = 'val,expected'
    vals = (
        (1, False),
        ('1', False),
        ([1], True),
        ((1, ), True),
        ({1: 2}, True),
        ({1, 2}, True),
    )
    ids = ('int', 'str', 'list', 'tuple', 'dict', 'set')

    return parametrize(names, vals, ids)


def param_it_erate():
    """Paramtrize test_it_erate"""
    names = 'val'
    vals = ([1, 2, ], ([1]), (1))
    ids = ('long', 'short', 'convert')

    return parametrize(names, vals, ids)
