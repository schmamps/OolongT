from collections import OrderedDict
from io import open as io_open
from json import dumps, load as json_load
from os import mkdir, unlink
from pathlib import Path
from re import sub

from generator.util.console import error as display_error
from oolongt.simple_io import load_json as load


TAB_SIZE = 11
OUTPUT_ROOT = Path(__file__).parent.parent.joinpath('output')


def get_output_path(comps, subdir=False):
    file_name = '.'.join(list(comps) + ['json'])
    subs = [x for x in [subdir, file_name] if x]

    return OUTPUT_ROOT.joinpath(*subs)


def cleanup(path):
    if path.exists():
        try:
            unlink(path)

        except IOError:
            display_error('unable to delete: ' + path)


def read(path):
    with io_open(path, 'r', encoding='utf8') as fp:
        data = json_load(fp, object_pairs_hook=OrderedDict)

        fp.close()

        return data


def write(path, data, kludge=False, subdir=''):
    # pylint: disable=no-member
    if not path.parent.exists():
        mkdir(str(path.parent.absolute()))

    with io_open(path, 'w', encoding='utf8') as fp:
        json_str = dumps(data, indent=TAB_SIZE)
        json_str = json_str.replace(' ' * TAB_SIZE, '\t')

        if kludge == 'keywords':
            patt = r'\{[\n\t]+("score".+,)\s+("count".+,)\s+("word".+)\s+\}'
            repl = r'{\1 \2 \3}'
            json_str = sub(patt, repl, json_str)

        fp.write(json_str)
        fp.close()
