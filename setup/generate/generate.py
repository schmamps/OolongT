import typing
from os import unlink
from pathlib import Path
from re import sub, split

from setup.util import console, json_data, PROC_TYPE
from tests.typedefs import Sample


def noop(val: typing.Any) -> typing.Any:
    return val


def process_keywords(json_str: str) -> str:
    patt = r'\{[\n\t]+("score".+,)\s+("count".+,)\s+("word".+)\s+\}'
    repl = r'{\1 \2 \3}'
    processed = sub(patt, repl, json_str)

    return processed


def get_samples(input_path: Path):
    for file in input_path.glob('*.json'):
        yield Sample(input_path, file.stem)


def get_final_path(output_path: Path, set_type: str, samp_name: str) -> Path:
    return output_path.joinpath(set_type, samp_name + '.json')


def cleanup(file_path: Path) -> None:
    console.info('deleting: {!r}', file_path)

    try:
        unlink(file_path)

        console.success('successfully deleted {!r}', file_path)

    except OSError:
        console.warn('unable to delete: {!r}', file_path)


def generate_sample(
        samp: Sample,
        set_type: str,
        handler: typing.Callable,
        input_path: Path,
        output_path: Path,
        pre_proc: PROC_TYPE,
        post_proc: PROC_TYPE
        ):
    try:
        console.group(samp.name)
        samp_data, file_path = handler(samp, input_path, output_path) # noqa # type: typing.Tuple[dict, str, bool]

        json_data.write(samp_data, file_path, pre_proc, post_proc)

        console.success(
            'saved {} {} to: ./{}',
            samp.name,
            set_type,
            '/'.join(split(r'[/\\]+', str(file_path.absolute()))[-3:]))

    except (OSError, UserWarning) as e:
        console.error(e)

        try:
            cleanup(file_path)
        except UnboundLocalError:
            pass

    except Exception as e:
        raise e

    finally:
        console.group_end()


def generate_set(
        set_type: str,
        handler: typing.Callable,
        input_path: Path,
        output_path: Path,
        pre_proc: PROC_TYPE = noop,
        post_proc: PROC_TYPE = noop):
    try:
        console.group(set_type.title())
        for samp in get_samples(input_path):
            generate_sample(
                samp,
                set_type,
                handler,
                input_path,
                output_path,
                pre_proc,
                post_proc)

    except Exception as e:
        raise e

    finally:
        console.group_end()
