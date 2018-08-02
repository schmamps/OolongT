from pytest import mark

from tests import helpers


@mark.parametrize(
    'text,kwargs,expected',
    [
        ('1234567890', {}, '1234567890'),
        ('123456789012345678901', {}, '12345678901234567...'),
        (['1234', '6789'], {}, '1234, 6789'),
        (['1234', '7890'], {'list_separator': '56'}, '1234567890'),
        ('1234567890', {'max_len': 9}, '123456...'),
        ('1234567890', {'max_len': 9, 'ellip': '!'}, '12345678!'),
    ],
    ids=helpers.pad_to_longest([
        'args: none           == "in"',
        'args: none           == "in" (truncated)',
        'args: none           == [in] (joined by comma)',
        'args: list_separator == [in] (joined creatively)',
        'args: max_len,       == "in" (truncated)',
        'args: max_len, ellip == "in" (truncated creatively)',
    ]))
def test_snip(text, kwargs, expected):
    received = helpers.snip(text, **kwargs)

    assert (received == expected), helpers.assert_ex(
        'snip',
        received,
        expected)


@mark.parametrize(
    'src,expected',
    [
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 0], True),
        ([], False),
    ],
    ids=helpers.pad_to_longest([
        'can be randomized',
        'cannot be randomized',
    ]))
def test_randomize_list(src, expected):
    received = helpers.randomize_list(src)

    assert src != received or not expected, helpers.assert_ex(
        'randomize_list',
        received,
        src
    )
