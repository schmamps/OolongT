"""Parametrize content tests"""

import typing
from re import split

from pytest import mark

from src.oolongt.content import Content, Document
from src.oolongt.io import load_json
# pylint: disable=unused-import
from src.oolongt.typings import StringList  # noqa: F401
# pylint: enable=unused-import
from tests.constants import DOC_PATH
from tests.helpers import pad_to_longest

BODY_IDX = 0
TITLE_IDX = 1
KW_IDX = 2
TEST_PATH = '/spam/eggs/bacon.ham'

ContentInit = typing.Tuple[str, str]
DocumentInit = typing.Tuple[str, str, str]


def split_any(val: typing.Any):
    """Split any value into a list of strings

    Arguments:
        val {typing.Any} -- any value

    Returns:
        StringList -- list of strings
    """
    is_iter = not isinstance(val, str) and hasattr(val, '__iter__')
    val = ','.join([str(ext) for ext in val]) if is_iter else str(val)

    return split(r'\s*,\s*', val.strip())


def compare_content_ex(
        content: Content,
        expected: tuple,
        title_comp: str) -> bool:
    """Compare Content (extended)

    Arguments:
        content {Content} -- instance of Content
        expected {tuple} -- expected properties
        title_comp {str} -- expected title

    Returns:
        bool -- content is expected
    """
    if content.body != expected[BODY_IDX]:
        return False

    return content.title == title_comp


def compare_content(content: Content, expected: tuple) -> bool:
    """Compare properties of `content` to values in `expected`

    Arguments:
        content {Content} -- instance of Content
        expected {tuple} -- expected properties

    Returns:
        bool -- content is expected
    """
    title_comp = expected[1]
    content_match = compare_content_ex(content, expected, title_comp)
    if not content_match:
        breakpoint()

    return content_match


def compare_document(doc: Document, expected: tuple) -> bool:
    """Compare properties of `doc` to values in `expected`

    Arguments:
        doc {Document} -- instance of Document
        expected {tuple} -- expected properties

    Returns:
        bool -- document is expected
    """
    title_comp = expected[TITLE_IDX]

    content_match = compare_content_ex(doc, expected, title_comp)
    path_match = (doc.path == expected[2])

    return content_match and path_match


def get_content(cls: Content, params: tuple) -> Content:
    """Initialize `cls` with `params`

    Arguments:
        cls {Content} -- Content (sub)class
        params {tuple} -- initialization params

    Returns:
        Content -- instance of Content
    """
    body, title = params

    return cls(body, title)


def get_document(cls: Document, params: tuple) -> Document:
    """Initialize `cls` with `params`

    Arguments:
        cls {Document} -- Document (sub)class
        params {tuple} -- initialization params

    Returns:
        Document -- instance of Document
    """
    body, title, path = params

    return cls(body, title, path)


def get_tests() -> typing.Generator[tuple, None, None]:
    """List basic test data and IDs

    Returns:
        typing.Generator[tuple, None, None] --
            [0]: ID, [1]: params, [2]: expected
    """
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


def get_test(test: tuple, has_path: bool) -> typing.Tuple[tuple, tuple]:
    """Get individual test data

    Arguments:
        test {tuple} -- single element of get_tests()
        has_path {bool} -- add document path

    Returns:
        typing.Tuple[tuple, tuple] -- (instance) params, expected
    """
    test_params = test[1]
    expected = test[2]

    if has_path:
        test_params.append(TEST_PATH)

    return tuple(test_params), tuple(expected)


def get_test_tuples(has_path: bool):
    """Get test parameters and IDs

    Arguments:
        has_path {bool} -- add document path

    Returns:
        typing.Tuple[typing.List[tuple], typing.List[str]] --
            test params, test IDs
    """
    params = [get_test(test, has_path) for test in get_tests()]
    ids = [test[0] for test in get_tests()]

    return params, pad_to_longest(ids)


def param_content(has_path: bool = False):
    """Parametrize for Content initialization

    Keyword Arguments:
        has_path {bool} -- add document path (default: {False})
    """
    params, ids = get_test_tuples(has_path)

    return mark.parametrize('params,expected', params, ids=ids)


def param_content_init(cls: Content):
    """Parametrize with initialized `cls` and expected properties

    Arguments:
        cls {Content} -- class to initialize
    """
    test_data, ids = get_test_tuples(False)

    params = [
        (get_content(cls, test_data[i][0]), test_data[i][1])
        for i in range(len(test_data))]

    return mark.parametrize('inst,expected', params, ids=ids)


def param_document():
    """Parametrize for Document initialization"""
    return param_content(True)


def get_doc_path(stem: str, ext: str):
    """Base function for getting sample file paths

    Arguments:
        stem {str} -- stem of sample path
        ext {str} -- extension to sample file

    Returns:
        str -- full path to sample
    """
    filename = '.'.join([stem, ext])

    return str(DOC_PATH.joinpath(filename))


def get_expected_doc(stem: str, path: str):
    """Get expected properties for sample named `stem`

    Arguments:
        stem {str} -- stem of sample
        path {str} -- path to sample

    Returns:
        tuple -- (body, title, path) of sample
    """
    json_path = get_doc_path(stem, 'json')
    data = load_json(json_path)

    body = data.get('body')
    title = data.get('title')

    return (body, title, path)


def param_document_init(
        cls: Document,
        ext: str,
        stems: typing.Any = 'basic'):
    """Parametrize with initialized `cls` and expected properties

    Arguments:
        cls {Document} -- class to initialize
        ext {str} -- extension of sample file

    Keyword Arguments:
        stems {typing.Any} -- stems of files for init (default: {'basic'})
    """
    ids = []
    params = []

    for stem in split_any(stems):
        path = get_doc_path(stem, ext)
        inst = cls(path)

        expected = get_expected_doc(stem, path)

        params.append((inst, expected))
        ids.append(stem)

    return mark.parametrize('inst,expected', params, ids=pad_to_longest(ids))


def permute_schemes(path: str) -> typing.Generator[tuple, None, None]:
    """Get tuples of ID hint and path to document (local and remote)

    Arguments:
        path {str} -- path to document

    Returns:
        typing.Generator[tuple, None, None] -- id hint, path
    """
    yield ('local', 'file://{}.{{}}'.format(path))
    yield ('remote', 'https:/{}.{{}}'.format(path))


def permute_ext(ext: str, always: typing.Any):
    """Get tuples of file extension, path extension, ID hint, and is_supported

    Arguments:
        ext {str} -- supported file extension
        always {typing.Any} -- override default is_supported
    """
    ext_x = 'FAIL'
    default_true = always is not False
    default_false = always is True

    yield (ext, ext, 'path-ext', default_true)
    yield (ext, ext_x, 'path-only', default_false)
    yield (ext_x, ext, 'ext-only', default_true)
    yield (ext_x, ext_x, 'all-wrong', default_false)


def param_supports(*exts: typing.Any, always: typing.Any = None):
    """Parametrize Document.supports() tests

    Keyword Arguments:
        always {typing.Any} -- override default test (default: {None})
    """
    ids = []  # type: StringList
    params = []  # type: typing.List[typing.Tuple[str, str, bool]]
    path = '/spam/eggs/bacon'
    for prefix, formatter in permute_schemes(path):
        for ext in split_any(exts):
            for path_ext, ext_ext, stub, truth in permute_ext(ext, always):
                ids.append('{}/{}/{}'.format(prefix, stub, ext or None))
                params.append((formatter.format(path_ext), ext_ext, truth))

    return mark.parametrize(
        'path,ext,expected', params, ids=pad_to_longest(ids))
