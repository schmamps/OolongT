import typing
from re import split

from pytest import mark

from src.oolongt.content import Content, Document
from src.oolongt.io import load_json
from src.oolongt.typedef import OPT_STR, STR_LIST
from tests.constants import DOC_PATH
from tests.helpers import pad_to_longest

BODY_IDX = 0
TITLE_IDX = 1
KW_IDX = 2
TEST_PARAMS = typing.List[typing.Any]
TEST_DATA = typing.Tuple[
    str,
    TEST_PARAMS,
    typing.List[typing.Union[str, STR_LIST]]]
TEST_PATH = '/spam/eggs/bacon.ham'

CONTENT_INIT_EXPECTED = typing.Tuple[str, str, STR_LIST]
DOC_INIT_EXPECTED = typing.Tuple[str, str, STR_LIST, str]


def split_any(exts: typing.Any):
    is_iter = not isinstance(exts, str) and hasattr(exts, '__iter__')
    exts = ','.join([str(ext) for ext in exts]) if is_iter else str(exts)

    return split(r'\s*,\s*', exts.strip())


def compare_content_ex(
        content: Content,
        expected: tuple,
        title_comp: str) -> bool:

    if content.body != expected[BODY_IDX]:
        return False

    return content.title == title_comp


def compare_content(content: Content, expected: tuple) -> bool:
    title_comp = expected[1]
    content_match = compare_content_ex(content, expected, title_comp)

    return content_match


def compare_document(doc: Document, expected: tuple, path=TEST_PATH):
    title_comp = expected[TITLE_IDX]

    content_match = compare_content_ex(doc, expected, title_comp)
    path_match = (doc.path == path)

    return content_match and path_match


def get_content(cls: Content, params: tuple) -> Content:
    body, title = params

    return cls(body, title)


def get_document(cls: Document, params: tuple) -> Document:
    body, title, path = params

    return cls(body, title, path)


def get_tests() -> typing.Generator[TEST_DATA, None, None]:
    yield (
        'body-None-simple',
        ['body', None],
        ['body', ''])

    yield (
        'BODY-title-simple',
        ['BODY', 'title'],
        ['BODY', 'title'])

    yield (
        'body-title-complex',
        [' body\n\t', '  \rTiTLe  '],
        ['body', 'TiTLe'])


def get_test(test: TEST_DATA, has_path: bool) -> typing.Tuple[tuple, tuple]:
    test_params = test[1]  # type: TEST_PARAMS
    expected = test[2]

    if has_path:
        test_params.append(TEST_PATH)

    return tuple(test_params), tuple(expected)


def param_content(has_path: bool = False):
    ids = [test[0] for test in get_tests()]
    params = [get_test(test, has_path) for test in get_tests()]

    return mark.parametrize('params,expected', params, ids=pad_to_longest(ids))


def param_document():
    return param_content(True)


def get_doc_path(stem: str, ext: str):
    filename = '.'.join([stem, ext])

    return str(DOC_PATH.joinpath(filename))


def get_expected_doc(stem: str, ext: str,):
    json_path = get_doc_path(stem, 'json')
    data = load_json(json_path)

    body = data.get('body')
    title = data.get('title')
    path = get_doc_path(stem, ext)

    return (body, title, path)


def param_document_init(
        cls: Document,
        ext: str,
        stems: typing.Any = 'basic'):
    ids = []
    params = []

    for stem in split_any(stems):
        expected = get_expected_doc(stem, ext)

        path = get_doc_path(stem, ext)
        inst = cls(path)

        ids.append(stem)
        params.append((inst, expected))

    return mark.parametrize('inst,expected', params, ids=pad_to_longest(ids))


def permute_schemes(path: str):
    yield ('local', 'file://{}.{{}}'.format(path))
    yield ('remote', 'https:/{}.{{}}'.format(path))


def permute_ext(ext: str, always: typing.Any):
    ext_x = 'FAIL'
    default_true = always is not False
    default_false = always is True

    yield (ext, ext, 'path-ext', default_true)
    yield (ext, ext_x, 'path-only', default_false)
    yield (ext_x, ext, 'ext-only', default_true)
    yield (ext_x, ext_x, 'all-wrong', default_false)


def param_supports(*exts: typing.Any, always: typing.Any = None):
    ids = []  # type: typing.List[str]
    params = []  # type: typing.List[typing.Tuple[str, str, bool]]
    path = '/spam/eggs/bacon'
    for prefix, formatter in permute_schemes(path):
        for ext in split_any(exts):
            for path_ext, ext_ext, stub, truth in permute_ext(ext, always):
                ids.append('{}/{}/{}'.format(prefix, stub, ext or None))
                params.append((formatter.format(path_ext), ext_ext, truth))

    return mark.parametrize(
        'path,ext,expected', params, ids=pad_to_longest(ids))
