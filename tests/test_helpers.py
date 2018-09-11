import typing
from pytest import mark

from tests.helpers import assert_ex, pad_to_longest, snip


@mark.parametrize(
    'text,kwargs,expected',
    [
        ('1234567890', {}, '1234567890'),
        ('123456789012345678901', {}, '12345678901234567...'),
        (['1234', '6789'], {}, '1234, 6789'),
        (['1234', '7890'], {'list_separator': '56'}, '1234567890'),
        ('1234567890', {'max_len': 9}, '123456...'),
        ('1234567890', {'max_len': 9, 'ellip': '!'}, '12345678!'), ],
    ids=pad_to_longest([
        'args: none           == "in"',
        'args: none           == "in" (truncated)',
        'args: none           == [in] (joined by comma)',
        'args: list_separator == [in] (joined creatively)',
        'args: max_len,       == "in" (truncated)',
        'args: max_len, ellip == "in" (truncated creatively)', ]))
def test_snip(
        text: str,
        kwargs: typing.Dict[str, typing.Any],
        expected: str
        ) -> None:
    received = snip(text, **kwargs)

    assert (received == expected), assert_ex(
        'snip',
        received,
        expected)
