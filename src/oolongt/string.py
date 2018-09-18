"""String helpers"""
import re
import typing
from unicodedata import normalize

from . import it
from .pipe import pipe
from .typings import StringList

AnyOrAnys = typing.Union[
    typing.Any, typing.List[typing.Any]]
StringOrStringIterator = typing.Union[
    str, typing.Iterator[str]]
StringOrStrings = typing.Union[
    str, StringList]


def cast(val: AnyOrAnys) -> StringOrStringIterator:
    """Cast member(s) of `val` as string

    Arguments:
        val {AnyOrAnys} -- value or values

    Returns:
        StringOrStringIterator -- `val` as string or strings
    """
    return map(str, val) if it.erable(val) else str(val)


def define_split(sep: str):
    """Define a string splitting function

    Arguments:
        sep {str} -- regex to split

    Returns:
        typing.Callable -- splitting function
    """
    def split_string(val: typing.Any) -> StringList:
        return re.split(sep, str(val))

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


def strip(val: StringOrStrings) -> typing.Union[str, typing.Iterator[str]]:
    """Trim str or strs in `val`

    Arguments:
        val {OptionalStringList} -- str or strs

    Returns:
        typing.Union[str, StringList] -- stripped str or strs
    """
    if it.erable(val):
        return (v.strip() for v in val)

    return str(val).strip()


def filter_empty(strs: StringList) -> typing.Iterable:
    """Remove empty strings from `strs`

    Arguments:
        strs {StringList} -- list of strings

    Returns:
        StringList -- list of non-empty strings
    """
    return (s for s in strs if s)


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
    pipeline.append(cast if it.erable(val) else define_split(sep))

    if strip_text:
        pipeline.append(strip)

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
