"""Parser Configuration Reader"""
import typing
from json import JSONDecodeError
from pathlib import Path

from nltk.corpus import stopwords

from ..constants import (
    BUILTIN, DEFAULT_IDEAL_LENGTH, DEFAULT_IDIOM, DEFAULT_LANGUAGE,
    DEFAULT_NLTK_STOPS, DEFAULT_USER_STOPS)
from ..io import load_json
from ..repr_able import ReprAble
from ..typings import DictOfAny, StringList

IdiomData = typing.Tuple[int, str, StringList]


def get_config_path(root: str, idiom: str) -> Path:
    """Get path to idiom config

    Arguments:
        root {str} -- root directory of idiom config
        idiom {str} -- basename of idiom config

    Returns:
        Tuple[Path, Path] -- pathlib.Path to file
    """
    root_path = Path(root)
    file_name = '{}.json'.format(idiom)

    return root_path.joinpath(file_name)


def get_stop_words(idiom_spec: DictOfAny, language: str) -> set:
    """List stop words based on idiom configuration

    Returns:
        set -- list of stop words
    """
    stop_cfg = {
        'nltk': DEFAULT_NLTK_STOPS,
        'user': DEFAULT_USER_STOPS, }  # type: DictOfAny
    stop_cfg.update(idiom_spec.get('stop_words', {}))
    use_nltk = bool(stop_cfg['nltk'])
    use_user = isinstance(stop_cfg['user'], list)

    nltk = stopwords.words(language) if use_nltk else []
    user = [str(word) for word in stop_cfg['user']] if use_user else []

    return set(nltk + user)


def parse_config(path: Path) -> typing.Tuple[int, str, StringList]:
    """Load defaults, override with loaded data

    Arguments:
        path {Path} -- path to config file

    Raises:
        ValueError -- unable to read file

    Returns:
        typing.Tuple[int, str, StringList] --
            ideal length, NLTK language, stop words
    """
    try:
        idiom_spec = load_json(path.absolute())

        ideal = idiom_spec.get(
            'ideal', DEFAULT_IDEAL_LENGTH)  # type: int
        language = idiom_spec.get(
            'language', DEFAULT_LANGUAGE)   # type: str
        stop_words = get_stop_words(
            idiom_spec, language)           # type: typing.Set[str]

    except (JSONDecodeError, AttributeError):
        raise ValueError('invalid config file: {!r}'.format(path))

    return int(ideal), str(language), list(stop_words)


def load_idiom(
        root: str = BUILTIN,
        idiom: str = DEFAULT_IDIOM) -> IdiomData:
    """Get class initialization data from `root`/`idiom`.json

    Arguments:
        root {str} -- root directory of idiom data
            (default: {parser.BUILTIN})
        idiom {str} -- basename of idiom file
            (default: {parser.DEFAULT_IDIOM})

    Raises:
        PermissionError -- directory traversal via idiom
        JSONDecodeError -- unable to load JSON from file

    Returns:
        IDIOM_DATA --
            tuple(ideal length, NLTK language, stop words)
    """
    root_path = Path(root)
    cfg_path = get_config_path(root, idiom)

    try:
        # pylint: disable=no-member
        cfg_path.resolve().relative_to(root_path.resolve())

    except (ValueError, OSError):
        raise PermissionError('directory traversal in idiom: ' + idiom)

    config = parse_config(cfg_path)

    return config


class ParserConfig(ReprAble):  # pylint: disable=too-few-public-methods
    """Parser configuration data"""
    def __init__(self, root: str, idiom: str) -> None:
        ideal, language, stop_words = load_idiom(root, idiom)

        self.ideal_sentence_length = ideal  # type: int
        self.language = language            # type: str
        self.stop_words = stop_words        # type: StringList
