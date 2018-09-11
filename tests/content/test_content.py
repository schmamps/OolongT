"""Test Content base content class"""
from pytest import mark

from src.oolongt.content.content import (
    Content, join_strs, norm_text, split_strs, strip_strs)
from src.oolongt.typings import OptionalString, StringList
from tests.helpers import pad_to_longest
from tests.params.content import (
    ContentInit, get_content, param_content, param_content_init)

EGGS = 'eggs'
SPAM = 'spam'
BACON = 'bacon'

JOIN_SPLIT_PARAMS = [
    ('', False, ['']),
    ('{} {} {}'.format(SPAM, EGGS, BACON), False, [SPAM, EGGS, BACON]),
    ('{},{},{}'.format(SPAM, EGGS, BACON), ',', [SPAM, EGGS, BACON]), ]
JOIN_SPLIT_IDS = ['empty', 'basic', 'custom']


@mark.parametrize(
    'str_list,expected',
    [(
        [SPAM, ' eggs', 'bacon ', ' spam '],
        [SPAM, 'eggs', BACON, SPAM], ), ],
    ids=pad_to_longest(
        [SPAM, ]))
def test_strip_strs(str_list: StringList, expected: StringList):
    """Test strip_strs

    Arguments:
        str_list {StringList} -- list of strings
        expected {StringList} -- stripped strings
    """
    received = strip_strs(str_list)

    assert received == expected


@mark.parametrize(
    'unsplit,sep,expected', JOIN_SPLIT_PARAMS, ids=JOIN_SPLIT_IDS)
def test_split_strs(unsplit: str, sep: str, expected: StringList):
    """Test split_strs

    Arguments:
        unsplit {str} -- input string
        sep {str} -- separator regex
        expected {StringList} -- expected StringList
    """
    received = split_strs(unsplit, sep) if sep else split_strs(unsplit)

    assert received == expected


@mark.parametrize(
    'expected,sep,str_list', JOIN_SPLIT_PARAMS, ids=JOIN_SPLIT_IDS)
def test_join_strs(expected: str, sep: str, str_list: StringList):
    """Test join_strs

    Arguments:
        expected {str} -- expected string
        sep {str} -- separator regex
        str_list {StringList} -- input StringList
    """
    received = join_strs(str_list, sep) if sep else join_strs(str_list)

    assert received == expected


@mark.parametrize(
    'text,expected',
    [(None, ''), (SPAM, SPAM), ('   ham ', 'ham')],
    ids=pad_to_longest(['None', SPAM, 'sloppy']))
def test_norm_text(text: OptionalString, expected: str):
    """Test norm_text

    Arguments:
        text {OptionalString} -- str or None
        expected {str} -- expected string
    """
    received = norm_text(text)

    assert received == expected


# pylint: disable=no-self-use
class TestContent:
    """Test Content class"""
    @param_content()
    def test_body(self, params: ContentInit, expected: tuple):
        """Test `body` property of instance

        Arguments:
            params {ContentInit} -- initialization params
            expected {tuple} -- expected body, title
        """
        inst = get_content(Content, params)

        assert inst.body == expected[0]

    @param_content()
    def test_title(self, params: ContentInit, expected: tuple):
        """Test `title` property of instance

        Arguments:
            params {ContentInit} -- initialization params
            expected {tuple} -- expected body, title
        """
        inst = get_content(Content, params)

        assert inst.title == expected[1]

    @param_content()
    def test___str__(self, params: ContentInit, expected: tuple):
        """Test string cast of instance

        Arguments:
            params {ContentInit} -- initialization params
            expected {tuple} -- expected body, title
        """
        inst = get_content(Content, params)

        assert str(inst) == expected[0]

    def _test_repr(self, inst: Content, expected: tuple):
        """Test repr() string of instance

        Arguments:
            inst {Content} -- initialization params
            expected {tuple} -- expected body, title
        """
        body, title = expected
        expected_str = '{}({!r}, {!r})'.format(
            inst.__class__.__name__, body, title)

        received = repr(inst)

        if received != expected_str:
            breakpoint()

        return received == expected_str

    @param_content_init(Content)
    def test___repr__(self, inst: Content, expected: tuple):
        """Test Content REPR

        Arguments:
            inst {Content} -- instance of Content
            expected {tuple} -- expected string
        """
        self._test_repr(inst, expected)
