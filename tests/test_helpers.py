from pytest import mark

from . import helpers


@mark.parametrize('text,kwargs,expected', [
    ('1234567890', {}, '1234567890'),
    ('123456789012345678901', {}, '12345678901234567...'),
    (['1234', '6789'], {}, '1234, 6789'),
    (['1234', '7890'], {'list_separator': '56'}, '1234567890'),
    ('1234567890', {'max_len': 9}, '123456...'),
    ('1234567890', {'max_len': 9, 'ellip': '!'}, '12345678!'),
])
def test_snip(text, kwargs, expected):
    received = helpers.snip(text, **kwargs)

    assert (received == expected), helpers.assert_ex(
        'snip',
        received,
        expected)


@mark.parametrize('src,expected', [
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 0], True),
    ([], False),
])
def test_randomize_list(src, expected):
    received = helpers.randomize_list(src)

    assert src != received or not expected, helpers.assert_ex(
        'randomize_list',
        received,
        src
    )


@mark.parametrize('left,right,kwargs,expected', [
    ({1: 1}, {1: 1}, {}, True),
    ({1: 1}, {1: 1, 2: 2}, {}, True),
    ({1: 1, 2: 2}, {1: 1}, {}, False),
    ({1: 1, 2: 2}, {1: 1}, {'keys': [1]}, True),
    ({1: 1, 2: 2}, {1: 1}, {'ignore': [1]}, False),
])
def test_compare_dict(left, right, kwargs, expected):
    received = helpers.compare_dict(left, right, **kwargs)

    assert (received == expected), helpers.assert_ex(
        'compare_dict',
        received,
        expected)
