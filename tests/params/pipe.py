"""Test pipe package params"""
from src.oolongt.pipe import noop
from tests.helpers import return_false, return_true
from tests.params.helpers import parametrize


def param_noop():
    """Parametrize `test_noop`"""
    names = 'expected'
    vals = ((''), (0), (True), (False), (None), )
    ids = ('empty', 'zero', 'true', 'false', 'none', )

    return parametrize(names, vals, ids)


def param_pipe():
    """Parametrize `test_pipe`"""
    names = 'init,pipeline,expected'
    vals = (
        (0, return_false, False),
        (0, (return_false, return_true), True),
        (0, (noop, (noop, noop), [noop, noop]), 0),
    )
    ids = ('simple', 'tuple', 'complex')

    return parametrize(names, vals, ids)
