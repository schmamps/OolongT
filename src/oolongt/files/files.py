"""Apply oolongt to files"""
import typing
from os.path import abspath
from pathlib import Path

import oolongt.text as main
from oolongt.constants import BUILTIN, DEFAULT_IDIOM, DEFAULT_LENGTH
from oolongt.files import application, text
from oolongt.typedefs import Content, ScoredSentence


def load_file(path: str) -> Content:
    """Get text contents of the file at `path`

    Arguments:
        path {str} -- path to document

    Raises:
        ValueError -- unable to read file

    Returns:
        Content -- contents of file
    """
    ext = Path(path).suffix

    try:
        func = text.plain

        if ext == '.doc':
            func = application.msword
        elif ext == '.docx':
            func = application.docx
        elif ext == '.pdf':
            func = application.pdf
        elif ext == '.rtf':
            func = application.rtf
        elif ext == '.htm' or '.html':
            func = text.html

        return func(path)

    except (OSError) as e:  # pylint: disable=invalid-name
        raise ValueError('Unable to read {!r} ({})'.format(abspath(path), e))


def prep_args(  # pylint: disable=too-many-arguments
        path: str,
        root: typing.Any,
        idiom: typing.Any,
        source: typing.Any,
        category: typing.Any,
        length: typing.Any = None) -> typing.Dict[str, typing.Any]:
    """Prepare arguments for passing to oolongt.text

    Arguments:
        path {str} -- path to document
        root {typing.Any} -- root of idiom directory
        idiom {typing.Any} -- name of idiom
        source {typing.Any} -- unused
        category {typing.Any} -- unused

    Keyword Arguments:
        length {typing.Any} --
            num/pct of sentences to return
            if applicable (default: {None})

    Returns:
        typing.Dict[str, typing.Any] -- keyword arguments for string functions
    """
    content = load_file(path)

    nominal_args = {
        'body': content.body,
        'title': content.title,
        'root': root,
        'idiom': idiom,
        'source': source,
        'category': category,
        'length': length, }

    return {
        key: val
        for key, val in nominal_args.items()
        if val is not None}


def score_body_sentences(
        path: str,
        root: typing.Any = BUILTIN,
        idiom: typing.Any = DEFAULT_IDIOM,
        source: typing.Any = None,
        category: typing.Any = None) -> typing.List[ScoredSentence]:
    """List and score every sentence in `body`

    Arguments:
        body {str} -- body of content
        title {str} -- title of content

    Keyword Arguments:
        root {str} -- root directory of idiom config
        idiom {str} -- basename of idiom config
        source {any} -- unused (default: {None})
        category {any} -- unused (default: {None})

    Returns:
        typing.List[ScoredSentence] --
            List of sentences with scoring and metadata
    """
    kwargs = prep_args(path, root, idiom, source, category)

    return main.score_body_sentences(**kwargs)


def summarize(  # pylint: disable=too-many-arguments
        path: str,
        length: float = DEFAULT_LENGTH,
        root: typing.Any = BUILTIN,
        idiom: typing.Any = DEFAULT_IDIOM,
        source: typing.Any = None,
        category: typing.Any = None) -> typing.List[str]:
    """Get `length` best sentences from `body` in content order

    if `length` < 1:
        len(return) = int(length * len(sentences))
    else:
        len(return) = min(length, len(sentences))

    Arguments:
        body {str} -- body of content
        title {str} -- title of content

    Keyword Arguments:
        length {float} -- sentences to return (>= 1) or
            coefficient of total (< 1) (default: {oolongt.DEFAULT_LENGTH})
        root {str} -- root directory of idiom data
            (default: {oolongt.BUILTIN})
        idiom {str} -- basename of idiom file
            (default: {oolongt.DEFAULT_IDIOM})
        source {any} -- unused (default: {None})
        category {any} -- unused (default: {None})

    Returns:
        list[str] -- top sentences in content order
    """
    kwargs = prep_args(path, root, idiom, source, category, length)

    return main.summarize(**kwargs)
