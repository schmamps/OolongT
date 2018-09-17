"""String helpers"""
import re
import typing
from unicodedata import normalize

from . import it
from .pipe import pipe
from .typings import StringList


def cast_value(val: typing.Any) -> str:
    """Cast `val` as str

    Arguments:
        val {typing.Any} -- any value

    Returns:
        str -- `val` as str
    """
    return str(val)


def cast_list(val: typing.Iterable[typing.Any]) -> typing.Iterable[str]:
    """Cast members of `val` as string

    Arguments:
        val {typing.Iterable[typing.Any]} -- iterable of values

    Returns:
        StringList -- `val` as strings
    """
    return map(cast_value, val)


def define_split(sep: str):
    """Define a string splitting function

    Arguments:
        sep {str} -- regex to split

    Returns:
        typing.Callable -- splitting function
    """
    def split_string(val: typing.Any) -> typing.List[str]:
        return re.split(sep, val)

    return split_string


def define_join(sep: str):
    """Define a string joining function

    Arguments:
        sep {str} -- string to join with

    Returns:
        typing.Callable -- joining function
    """
    def join_string(vals: typing.Iterable) -> str:
        return sep.join([str(val) for val in vals])

    return join_string


def strip_str(val: str) -> str:
    """Return `val.strip()`

    Arguments:
        val {str} -- string value

    Returns:
        str -- stripped string
    """
    return val.strip()


def strip_strs(strs: StringList) -> typing.Iterable:
    """Trim items of `strs`

    Arguments:
        strs {StringList} -- [description]

    Returns:
        StringList -- [description]
    """
    return map(strip_str, strs)


def filter_empty(strs: StringList) -> typing.Iterable:
    """Remove empty strings from `strs`

    Arguments:
        strs {StringList} -- list of strings

    Returns:
        StringList -- list of non-empty strings
    """
    return filter(bool, strs)


def split(
        val: typing.Any,
        sep: str = r'[,\s]+',
        strip_text: bool = True,
        allow_empty: bool = False) -> typing.Iterable[str]:
    """Split any value into a list of strings

    Arguments:
        val {typing.Any} -- any value

    Keyword Arguments:
        sep {str} - character to split by
        strip_text {bool} - remove leading and trailing whitespace
        allow_empty {bool} - allow empty strings

    Returns:
        StringList -- list of strings
    """
    pipeline = []  # type: typing.List[typing.Callable]
    pipeline.append(cast_list if it.erable(val) else define_split(sep))

    if strip_text:
        pipeline.append(strip_strs)

    if not allow_empty:
        pipeline.append(filter_empty)

    return pipe(val, *pipeline)


def norm_nfkd(text: str) -> str:
    """Normalize text

    Arguments:
        text {str} -- input text

    Returns:
        bytes -- [description]
    """
    return normalize('NFKD', text)


def encode_ascii(text: str) -> bytes:
    """Encode `text` in ascii

    Arguments:
        text {str} -- input text

    Returns:
        bytes -- encoded text
    """
    return text.encode('ascii', 'ignore')


def decode_utf8(text: bytes) -> str:
    """Decode `text` as UTF-8 string

    Arguments:
        bytes {text} -- ascii-encoded bytes

    Returns:
        str -- decoded text
    """
    return text.decode('utf-8')


def simplify(text: str) -> str:
    """Get low-value character representation of string

    Arguments:
        text {str} -- UTF-8 encoded string

    Returns:
        str -- string with low value characters
    """
    return pipe(text, norm_nfkd, encode_ascii, decode_utf8)
