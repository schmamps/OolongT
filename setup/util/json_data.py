import typing
from collections import OrderedDict
from io import open as io_open
from json import dumps, load as json_load
from os import makedirs
from pathlib import Path

from setup.util import PROC_TYPE
from src.oolongt.pipe import pipe


def noop(val: typing.Any) -> typing.Any:
    return noop


def read(path: Path) -> OrderedDict:
    with io_open(str(path), 'r', encoding='utf-8') as fp:
        data = json_load(fp, object_pairs_hook=OrderedDict)

    return data


def dump_data(data: typing.Dict) -> str:
    return dumps(data, indent='\t')


def write(
        data: typing.Union[typing.Dict, OrderedDict],
        path: Path,
        pre_proc: PROC_TYPE = noop,
        post_proc: PROC_TYPE = noop
        ) -> None:
    makedirs(str(path.parent), exist_ok=True)
    json_str = pipe(data, pre_proc, dump_data, post_proc)  # type: str

    with io_open(path, 'w', encoding='utf8') as fp:
        fp.write(json_str)
