from io import open as io_open
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


def prop(obj, prop, fmt='s'):
    val = obj[prop]
    if isinstance(val, str):
        val = '"{0}"'.format(val)

    formatter = '\t\t\t"{{0}}": {{1:{0}}}'.format(fmt)
    formatted = formatter.format(prop, val)

    return formatted
