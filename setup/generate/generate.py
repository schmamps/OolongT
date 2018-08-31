"""Generate Test Data"""
import typing
from os import unlink
from pathlib import Path
from re import sub, split

from setup.util import console, json_data, PROC_TYPE
from tests.typedefs import Sample


def noop(val: typing.Any) -> typing.Any:
    """Return input value

    Arguments:
        val {typing.Any} -- any value

    Returns:
        typing.Any -- input value
    """
    return val


def process_keywords(json_str: str) -> str:
    """Condense keyword data into fewer lines

    Arguments:
        json_str {str} -- JSON

    Returns:
        str -- condensed string
    """
    patt = r'\{[\n\t]+("score".+,)\s+("count".+,)\s+("word".+)\s+\}'
    repl = r'{\1 \2 \3}'
    processed = sub(patt, repl, json_str)

    return processed


def get_samples(input_path: Path):
    """Get `Sample`s from specified path

    Arguments:
        input_path {Path} -- path to Sample files
    """
    for file in input_path.glob('*.json'):
        yield Sample(input_path, file.stem)


def get_final_path(output_path: Path, set_type: str, samp_name: str) -> Path:
    """Get path of output file

    Arguments:
        output_path {Path} -- root of output path
        set_type {str} -- data set type
        samp_name {str} -- name of sample

    Returns:
        Path -- complete path to output file
    """
    return output_path.joinpath(set_type, samp_name + '.json')


def cleanup(file_path: Path):
    """Delete `file_path` (lazy)

    Arguments:
        file_path {Path} -- path to file
    """
    console.info('deleting: {!r}', file_path)

    try:
        unlink(file_path)

        console.success('successfully deleted {!r}', file_path)

    except OSError:
        console.warn('unable to delete: {!r}', file_path)


def generate_sample(  # pylint: disable=too-many-arguments
        samp: Sample,
        set_type: str,
        handler: typing.Callable,
        input_path: Path,
        output_path: Path,
        pre_proc: PROC_TYPE,
        post_proc: PROC_TYPE):
    """Generate JSON for a sample

    Arguments:
        samp {Sample} -- sample data
        set_type {str} -- data set type
        handler {typing.Callable} -- data processor
        input_path {Path} -- input path
        output_path {Path} -- output path
        pre_proc {PROC_TYPE} -- data dict pre-processor
        post_proc {PROC_TYPE} -- output JSON post-processor

    Raises:
        Exception -- unhandled error during generation
    """
    try:
        console.group(samp.name)
        samp_data, file_path = handler(samp, input_path, output_path)  # noqa # type: typing.Tuple[dict, str] # pylint: disable=line-too-long

        json_data.write(samp_data, file_path, pre_proc, post_proc)

        console.success(
            'saved {} {} to: ./{}',
            samp.name,
            set_type,
            '/'.join(split(r'[/\\]+', str(file_path.absolute()))[-3:]))

    except (OSError, UserWarning) as err:
        console.error(err)

        try:
            cleanup(file_path)
        except UnboundLocalError:
            pass

    except Exception as err:
        raise err

    finally:
        console.group_end()


def generate_set(  # pylint: disable=too-many-arguments
        set_type: str,
        handler: typing.Callable,
        input_path: Path,
        output_path: Path,
        pre_proc: PROC_TYPE = noop,
        post_proc: PROC_TYPE = noop):
    """Generate data set for the samples

    Arguments:
        set_type {str} -- kind of data set
        handler {typing.Callable} -- data processor
        input_path {Path} -- input path
        output_path {Path} -- output path

    Keyword Arguments:
        pre_proc {PROC_TYPE} -- data dict pre-processor (default: {noop})
        post_proc {PROC_TYPE} -- output JSON post-processor (default: {noop})

    Raises:
        Exception -- unhandled error during generation
    """
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

    except Exception as err:
        raise err

    finally:
        console.group_end()
