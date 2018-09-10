"""Pipeline functions"""
import typing


def pipe(data: typing.Any, *pipeline) -> typing.Any:
    """Run `data` through `pipeline` list (left-to-right)

    Arguments:
        data {typing.Any} -- any data
        funcs {typing.Callable} -- functions to run

    Returns:
        typing.Any -- result of functions
    """
    for segment in pipeline:
        if hasattr(segment, '__iter__'):
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
