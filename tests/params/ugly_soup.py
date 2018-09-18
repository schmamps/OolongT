"""UglySoup test parameters"""
from src.oolongt.io import load_json, read_file
from src.oolongt.ugly_soup import UglySoup
from src.oolongt.ugly_soup.ugly_query import get_text
from tests.constants import DOC_PATH
from tests.helpers import return_false, return_true
from tests.params.helpers import parametrize

MARKUP = read_file(DOC_PATH.joinpath('intermed.html'))
SOUP = UglySoup(MARKUP, features='html.parser')
DOC = load_json(DOC_PATH.joinpath('intermed.json'))

BODY_DIV_P = ['body', 'div', 'p']
TEST_TAGS = (
    (BODY_DIV_P, BODY_DIV_P, return_true, True),
    ([' body', ' div ', ' p'], BODY_DIV_P, return_false, False),
    ('body,div,p', BODY_DIV_P, return_true, True),
    ('body, div, p', BODY_DIV_P, return_false, False),
    (' body, div ,  p', BODY_DIV_P, return_true, True),
)
TEST_IDS = (
    'simple-list-true',
    'sloppy-list-false',
    'simple-str-true',
    'comfy-str-false',
    'sloppy-str-true',
)


def param_get_text():
    """Parametrize `test_get_text`"""
    names = 'tag,expected'
    vals = (
        ('header', 'Header'),
        ('main', DOC['body']),
        ('footer', 'Footer'),
    )
    ids = ('header', 'main', 'footer')

    return parametrize(names, vals, ids)


def param_test():
    """Parametrize `test_test`"""
    names = 'tags,tester,expected'
    vals = (
        ('main', get_text, DOC['body']),
        ('style', get_text, None),
        ('input', get_text, None),
    )
    ids = ('main', 'style', 'input', )

    return parametrize(names, vals, ids)


def param___repr__():
    """Parametrize `test___repr__`"""
    names = 'args'
    vals = (('div', ), )
    ids = ('basic', )

    return parametrize(names, vals, ids)


def param__query():
    """Parametrize `test_query`"""
    names = 'kwargs,expected'
    vals = (
        ({'tags': 'div'}, None),
        ({'tags': 'div, main'}, DOC['body']),
        ({'tags': 'div, main', 'tester': return_true}, True),
    )
    ids = ('none', 'text', 'func')

    return parametrize(names, vals, ids)


def param_query():
    """Parametrize `test_query`"""
    names = 'tags,kwargs,expected'
    vals = (
        (['div'], {}, ''),
        (['div'], {'default': 'spam'}, 'spam'),
        (['div', 'main', 'header'], {'default': 'spam'}, DOC['body']),
    )
    ids = ('use-default', 'set-default', 'find-value', )

    return parametrize(names, vals, ids)
