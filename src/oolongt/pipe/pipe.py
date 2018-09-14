"""Pipeline functions"""
import typing

from ..misc import is_iter_not_str


def pipe(data: typing.Any, *pipeline) -> typing.Any:
    """Run `data` through `pipeline` list (left-to-right)

    Arguments:
        data {typing.Any} -- any data
        funcs {typing.Callable} -- functions to run

    Returns:
        typing.Any -- result of functions
    """
    for segment in pipeline:
        if is_iter_not_str(segment):
            data = pipe(data, *segment)

        else:
            data = segment(data)

    return data


def noop(data: typing.Any) -> typing.Any:
    """Return the input value

    Arguments:
        data {typing.Any} -- any value

    Returns:
        typing.Any -- input value
    """
    return data
