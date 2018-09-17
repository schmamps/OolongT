from .helpers import parametrize

LIST_TEST_INT = list(range(1, 6))
LIST_TEST_STR = [str(x) for x in LIST_TEST_INT]
STR_TEST_SPACES = ' '.join(LIST_TEST_STR)
STR_TEST_COMMAS = ','.join(LIST_TEST_STR)
STR_TEST_CSV = '1 2, 3\t4, \t5'
ALPHA_SIMPLE = 'abcdefghijklmnopqrstuvwxyz'
ALPHA_COMPLEX = 'åbçdéfghîjklmnöpqrštùvwxyz'


def pad(val: str, spaces: int=2):
    pad_str = ' ' * spaces
    return '{0}{1}{0}'.format(pad_str, val)


def param_cast_list():
    """Parametrize `test_cast_list`"""
    names = 'val,expected'
    vals = (
        (LIST_TEST_INT, LIST_TEST_STR),
        ('12345', LIST_TEST_STR),  # sorry!
    )
    ids = ('int', 'oops', )

    return parametrize(names, vals, ids)


def param_define_split_join():
    """Parametrize `test_define_split` and `test_define_join`"""
    names = 'sep,str_val,list_val'
    vals = (
        (' ', STR_TEST_SPACES, LIST_TEST_STR),
        (',', STR_TEST_COMMAS, LIST_TEST_STR),
    )
    ids = ('spaces', 'commas', )

    return parametrize(names, vals, ids)


def param_strip_str():
    """Parametrize `test_strip_str`"""
    names = 'val,expected'
    vals = (
        (STR_TEST_SPACES, STR_TEST_SPACES),
        ('    {}'.format(STR_TEST_SPACES), STR_TEST_SPACES),
        ('{}    '.format(STR_TEST_COMMAS), STR_TEST_COMMAS),
        ('  {}  '.format(STR_TEST_CSV), STR_TEST_CSV),
    )
    ids = ('none', 'left', 'right', 'both', )

    return parametrize(names, vals, ids)


def param_strip_strs():
    """Parametrize `test_strip_strs`"""
    names = 'val,expected'
    vals = (
        (LIST_TEST_STR, LIST_TEST_STR),
        ([pad(num) for num in LIST_TEST_STR], LIST_TEST_STR),
    )
    ids = ('none', 'both', )

    return parametrize(names, vals, ids)


def param_filter_empty():
    """Parametrize `test_filter_empty`"""
    names = 'val,expected'
    vals = (
        (LIST_TEST_STR, LIST_TEST_STR),
        (('1', '', '2', '', '', '3', '4', '5'), LIST_TEST_STR),
    )
    ids = ('none', 'some', )

    return parametrize(names, vals, ids)


def param_split():
    """Parametrize `test_split`"""
    names = 'kwargs,expected'
    vals = (({}, []), )
    ids = ('ayy', )

    vals = [({}, None), ({}, None), ]
    ids = ['ayy', 'lmao']

    return parametrize(names, vals, ids)


def param_simplify():
    """Parametrize `test_simplify`"""
    names = 'val,expected'
    vals = (
        (ALPHA_SIMPLE, ALPHA_SIMPLE),
        (ALPHA_COMPLEX, ALPHA_SIMPLE),
    )
    ids = ('simple', 'complex', )

    return parametrize(names, vals, ids)
