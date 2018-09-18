"""Pipeline functions"""
import typing

from . import it


def pipe(data: typing.Any, *pipeline) -> typing.Any:
    """Run `data` through `pipeline` list (left-to-right)

    Arguments:
        data {typing.Any} -- any data
        *pipeline {callable(s)} -- callables to run

    Returns:
        typing.Any -- result of functions
    """
    for line in pipeline:
        data = pipe(data, *line) if it.erable(line) else line(data)

    return data


def noop(data: typing.Any) -> typing.Any:
    """Return the input value

    Arguments:
        data {typing.Any} -- any value

    Returns:
        typing.Any -- input value
    """
    return data
