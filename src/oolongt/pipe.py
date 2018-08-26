import typing


def pipe(data: typing.Any, *args):
    for arg in args:
        if isinstance(arg, (list, tuple)):
            data = pipe(data, *arg)

        else:
            data = arg(data)

    return data
