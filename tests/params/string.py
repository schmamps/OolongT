"""String module test parameters"""
from .helpers import parametrize

LIST_TEST_INT = list(range(1, 6))
LIST_TEST_STR = [str(x) for x in LIST_TEST_INT]
STR_TEST_SPACES = ' '.join(LIST_TEST_STR)
STR_TEST_COMMAS = ','.join(LIST_TEST_STR)
STR_TEST_CSV = '1 2, 3\t4, \t5'
ALPHA_SIMPLE = 'abcdefghijklmnopqrstuvwxyz'
ALPHA_COMPLEX = 'åbçdéfghîjklmnöpqrštùvwxyz'


def pad(val: str, spaces: int = 2) -> str:
    """Pad val on left and right with `spaces` whitespace chars

    Arguments:
        val {str} -- string to pad

    Keyword Arguments:
        spaces {int} -- number of spaces to pad on either side (default: {2})

    Returns:
        str -- padded string
    """
    pad_str = ' ' * spaces

    return '{0}{1}{0}'.format(pad_str, val)


def param_cast():
    """Parametrize `test_cast`"""
    names = 'val,expected'
    vals = (
        (1, '1', ),
        ('a', 'a'),
        (LIST_TEST_INT, LIST_TEST_STR),
        ('12345', LIST_TEST_STR),  # sorry!
    )
    ids = ('solo-int', 'solo-str', 'list-int', 'oops', )

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


def param_strip():
    """Parametrize `test_strip`"""
    names = 'val,expected'
    vals = (
        (STR_TEST_SPACES, STR_TEST_SPACES),
        ('    {}'.format(STR_TEST_SPACES), STR_TEST_SPACES),
        ('{}    '.format(STR_TEST_COMMAS), STR_TEST_COMMAS),
        ('  {}  '.format(STR_TEST_CSV), STR_TEST_CSV),
        (LIST_TEST_STR, LIST_TEST_STR),
        ([pad(num) for num in LIST_TEST_STR], LIST_TEST_STR),
    )
    ids = ('1-none', '1-left', '1-right', '1-center', '[]-none', '[]-both', )

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
    names = 'val,kwargs,expected'
    vals = (
        (
            LIST_TEST_INT,
            {},
            LIST_TEST_STR,
        ),
        (
            '|'.join(LIST_TEST_STR),
            {},
            ['|'.join(LIST_TEST_STR)],
        ),
        (
            '|'.join(LIST_TEST_STR),
            {'sep': r'\|'},
            LIST_TEST_STR,
        ),
        (
            ' 1| 2 | 3  |  4  |  5   ',
            {'sep': r'\|', },
            LIST_TEST_STR,
        ),
        (
            ' 1| 2 | 3  |  4  |  5   ',
            {'sep': r'\|', 'strip_text': False, },
            [' 1', ' 2 ', ' 3  ', '  4  ', '  5   '],
        ),
        (
            ' 1|| 2 | | 3  |  |  4  |   |  5   ',
            {'sep': r'\|', },
            LIST_TEST_STR,
        ),
        (
            ' 1|| 2 | | 3  |  |  4  |   |  5   ',
            {'sep': r'\|', 'allow_empty': True},
            ['1', '', '2', '', '3', '', '4', '', '5'],
        ),
        (
            ' 1|| 2 | | 3  |  |  4  |   |  5   ',
            {'sep': r'\|', 'strip_text': False, 'allow_empty': True},
            [' 1', '', ' 2 ', ' ', ' 3  ', '  ', '  4  ', '   ', '  5   '],
        ),
    )
    ids = (
        'defaults',
        'sep_default',
        'sep_custom',
        'strip_default',
        'strip_disabled',
        'allow_default',
        'allow_enabled',
        'all_options',
    )

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
