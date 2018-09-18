"""Iterable functions"""
import typing


def it_erable(val: typing.Any) -> bool:
    """Determine if `val` is a non-string iterable

    Arguments:
        val {typing.Any} -- any value

    Returns:
        bool -- value is nont-string iterable
    """
    return not isinstance(val, str) and hasattr(val, '__iter__')


def it_erate(val: typing.Any) -> typing.Tuple[typing.Any]:
    """Cast `val` as an iterable

    Arguments:
        val {typing.Any} -- any value

    Returns:
        typing.Iterable -- value as iterable
    """
    return val if it_erable(val) else (val, )
