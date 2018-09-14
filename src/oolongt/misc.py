"""helpers"""
import typing


def is_iter_not_str(val: typing.Any) -> bool:
    """Determine whether `val` is iterable (and not as chars of string)

    Arguments:
        val {typing.Any} -- any value

    Returns:
        bool -- val is iterable, but not string
    """
    return not isinstance(val, str) and hasattr(val, '__iter__')
