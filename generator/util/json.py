from io import open as io_open
from json import dumps
from os import mkdir
from pathlib import Path

from oolongt.simple_io import load_json as load


def create(major, minor):
    root = Path(__file__).parent.parent.joinpath('output')

    # pylint: disable=no-member
    if not root.exists():
        mkdir(str(root.absolute()))

    return io_open(
        root.joinpath('.'.join([minor, major, 'json'])), 'w', encoding='utf8')


def open(key, wrap):
    opened = '{{\n\t"{0}": '.format(key)

    if wrap:
        opened += wrap + '\n'

    return opened


def close(wrap):
    closed = '\n}'

    if wrap:
        closed = '\n\t{0}'.format(wrap) + closed

    return closed


def kv_pair(obj, prop, fmt='s', alt_key=False):
    key = dumps(alt_key or prop)
    val = dumps(obj[prop]) if (fmt == 's') else obj[prop]

    template = '{{0}}: {{1:{0}}}'.format(fmt)
    formattted = template.format(key, val)

    return formattted
