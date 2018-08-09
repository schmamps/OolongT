"""Parser Configuration Reader"""
import typing
from json import JSONDecodeError
from pathlib import Path

from nltk.corpus import stopwords

from oolongt.constants import (BUILTIN, DEFAULT_IDEAL_LENGTH, DEFAULT_LANG,
                               DEFAULT_NLTK_LANGUAGE, DEFAULT_NLTK_STOPS,
                               DEFAULT_USER_STOPS)
from oolongt.simple_io import load_json
from oolongt.typedefs.repr_able import ReprAble

CFG_TUPLE = typing.Tuple[int, str, typing.List[str]]


def get_config_paths(root: str, lang: str) -> typing.Tuple[Path, Path]:
    """Get path to language config

    Arguments:
        root {str} -- root directory of language config
        lang {str} -- basename of language config

    Returns:
        Tuple[Path, Path] -- pathlib.Path to file
    """
    root_path = Path(root)
    return root_path.joinpath(lang + '.json'), root_path


def get_stop_words(lang_spec: dict, nltk_language: str) -> set:
    """List stop words based on language configuration

    Returns:
        set -- list of stop words
    """
    stop_cfg = {
        'nltk': DEFAULT_NLTK_STOPS,
        'user': DEFAULT_USER_STOPS, }  # type: typing.Dict[str, typing.Any]
    stop_cfg.update(lang_spec.get('stop_words', {}))
    use_nltk = bool(stop_cfg['nltk'])
    use_user = isinstance(stop_cfg['user'], list)

    nltk = stopwords.words(nltk_language) if use_nltk else []
    user = [str(word) for word in stop_cfg['user']] if use_user else []

    return set(nltk + user)


def parse_config(path: Path) -> CFG_TUPLE:
    """Load defaults, override with loaded data

    Arguments:
        path {Path} -- path to config file

    Raises:
        ValueError -- unable to read file

    Returns:
        typing.Tuple[int, str, typing.List[str]] --
            ideal length, NLTK language, stop words
    """
    try:
        lang_spec = load_json(path.absolute())

        ideal = lang_spec.get(
            'ideal', DEFAULT_IDEAL_LENGTH)           # type: int
        nltk_language = lang_spec.get(
            'nltk_language', DEFAULT_NLTK_LANGUAGE)  # type: str
        stop_words = get_stop_words(
            lang_spec, nltk_language)                # type: typing.Set[str]

    except (JSONDecodeError, AttributeError):
        raise ValueError('invalid config file: {!r}'.format(path))

    return int(ideal), str(nltk_language), list(stop_words)


def load_language(root: str = BUILTIN, lang: str = DEFAULT_LANG) -> CFG_TUPLE:
    """Get class initialization data from `root`/`lang`.json

    Arguments:
        root {str} -- root directory of language data
            (default: {parser.BUILTIN})
        lang {str} -- basename of language file
            (default: {parser.DEFAULT_LANG})

    Raises:
        PermissionError -- directory traversal via lang
        JSONDecodeError -- unable to load JSON from file

    Returns:
        typing.Tuple[int, str, typing.List[str]] --
            ideal length, NLTK language, stop words
    """
    cfg_path, root_path = get_config_paths(root, lang)

    try:
        # pylint: disable=no-member
        cfg_path.resolve().relative_to(root_path.resolve())

    except (ValueError, OSError):
        raise PermissionError('directory traversal in lang: ' + lang)

    config = parse_config(cfg_path)

    return config


class ParserConfig(ReprAble):
    def __init__(self, root: str, lang: str) -> None:
        ideal, nltk_language, stop_words = load_language(root, lang)

        self.ideal_sentence_length = ideal  # type: int
        self.nltk_language = nltk_language  # type: str
        self.stop_words = stop_words        # type: typing.List[str]
