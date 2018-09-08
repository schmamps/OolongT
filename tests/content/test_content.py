"""Test Content base content class"""
import typing  # noqa: F401

from pytest import mark

from src.oolongt.content.content import Content, norm_text, strip_strs
from tests.helpers import pad_to_longest, remove_nones
from tests.params.content import get_content, param_content

BODY = 'spam'
TITLE = 'bacon'


def get_init(body=BODY, title=TITLE, path=None) -> Content:
    kwargs = {'body': body, 'title': title, 'path': path}

    return remove_nones(kwargs)


def get_repr(path: typing.Any):
    return 'Content({!r}, {!r}, {!r}, path={!r})'.format(
        BODY, TITLE.title(), KWS, path)


@mark.parametrize(
    'input,expected',
    [(
        ['spam', ' eggs', 'bacon ', ' spam '],
        ['spam', 'eggs', 'bacon', 'spam'], ), ],
    ids=pad_to_longest(
        ['spam', ]))
def test_strip_strs(input, expected):
    received = strip_strs(input)

    assert received == expected


@mark.parametrize(
    'input,expected',
    [(None, ''), ('spam', 'spam'), ('   ham ', 'ham')],
    ids=pad_to_longest(['None', 'spam', 'sloppy']))
def test_norm_text(input, expected):
    received = norm_text(input)

    assert received == expected


class TestContent:
    @param_content()
    def test_body(self, params, expected):
        """Test `body` property of instance

        Arguments:
            params {tuple} -- initialization params
            expected {tuple} -- expected body, title
        """
        inst = get_content(Content, params)

        assert inst.body == expected[0]

    @param_content()
    def test_title(self, params, expected):
        """Test `title` property of instance

        Arguments:
            params {tuple} -- initialization params
            expected {tuple} -- expected body, title
        """
        inst = get_content(Content, params)

        assert inst.title == expected[1]

    @param_content()
    def test___str__(self, params, expected):
        """Test string cast of instance

        Arguments:
            params {tuple} -- initialization params
            expected {tuple} -- expected body, title
        """
        inst = get_content(Content, params)

        assert str(inst) == expected[0]

    def _test_repr(self, cls: Content, params, expected):
        """Test repr() string of instance

        Arguments:
            params {tuple} -- initialization params
            expected {tuple} -- expected body, title
        """
        body, title = expected
        expected = '{}({!r}, {!r})'.format(
           cls.__name__, body, title)

        inst = get_content(cls, params)
        received = repr(inst)

        assert received == expected

    @param_content()
    def test___repr__(self, params, expected):
        self._test_repr(Content, params, expected)
