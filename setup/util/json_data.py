"""JSON data utility"""
import typing
from collections import OrderedDict
from io import open as io_open
from json import dumps
from json import load as json_load
from os import makedirs
from pathlib import Path

from setup.typings import ProcType
from src.oolongt.pipe import pipe


def noop(val: typing.Any) -> typing.Any:
    """Return input value

    Arguments:
        val {typing.Any} -- any value

    Returns:
        typing.Any -- input value
    """
    return val


def read(path: Path) -> OrderedDict:
    """Get contents of JSON at `path`

    Arguments:
        path {Path} -- path to file

    Returns:
        OrderedDict -- JSON data
    """
    with io_open(str(path), 'r', encoding='utf-8') as stream:
        data = json_load(stream, object_pairs_hook=OrderedDict)

    return data


def dump_data(data: typing.Dict) -> str:
    """Convert dictionary to JSON string

    Arguments:
        data {typing.Dict} -- data dictionary

    Returns:
        str -- JSON string
    """
    return dumps(data, indent='\t')


def write(
        data: typing.Union[typing.Dict, OrderedDict],
        path: Path,
        pre_proc: ProcType = noop,
        post_proc: ProcType = noop):
    """Write `data` to `path` with optional pre- and post-processsors

    Arguments:
        data {typing.Union[typing.Dict, OrderedDict]} -- data dictionary
        path {Path} -- path to write

    Keyword Arguments:
        pre_proc {ProcType} -- process `data` dict w/ func (default: {noop})
        post_proc {ProcType} -- process JSON string w/ func (default: {noop})
    """
    makedirs(str(path.parent), exist_ok=True)
    json_str = pipe(data, pre_proc, dump_data, post_proc)  # type: str

    with io_open(path, 'w', encoding='utf8') as stream:
        stream.write(json_str)
