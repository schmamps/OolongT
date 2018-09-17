"""Pipeline functions"""
import typing


def pipe(data: typing.Any, *pipeline: typing.Callable) -> typing.Any:
    """Run `data` through `pipeline` list (left-to-right)

    Arguments:
        data {typing.Any} -- any data
        *pipeline {callable} -- callables to run

    Returns:
        typing.Any -- result of functions
    """
    for call in pipeline:
        data = call(data)

    return data


def noop(data: typing.Any) -> typing.Any:
    """Return the input value

    Arguments:
        data {typing.Any} -- any value

    Returns:
        typing.Any -- input value
    """
    return data
