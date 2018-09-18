"""Text test params"""
from tests.constants import SAMPLES
from tests.params.helpers import parametrize


def param_summarize():
    """Parametrize `test_summarize`"""
    names = 'sample_name,limit'
    vals = []
    ids = []

    for sample_name in SAMPLES:
        for limit in range(1, 8, 2):
            vals.append((sample_name, limit, ))
            ids.append('{}-{}'.format(sample_name, limit))

    return parametrize(names, vals, ids)


def param_get_slice_length():
    """Parametrize `test_get_slice_length`"""
    names = 'nominal,total,expected'
    vals = (
        (20, 1000, 20),
        (1001, 1000, 1000),
        (.1, 1000, 100),
        (0, 0, ValueError),
    )
    ids = (
        'abs-within_limit',
        'abs-above_limit',
        'relative-of_total',
        'invalid_value',
    )

    return parametrize(names, vals, ids)
