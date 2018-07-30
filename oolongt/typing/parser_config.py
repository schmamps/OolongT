"""Parser Configuration Reader"""
from json import JSONDecodeError
from pathlib import Path

from nltk.corpus import stopwords

from oolongt.constants import (
    BUILTIN, DEFAULT_LANG,
    DEFAULT_CUSTOM_STOPS, DEFAULT_INITIAL_STOPS,
    DEFAULT_IDEAL_LENGTH, DEFAULT_NLTK_LANGUAGE,)
from oolongt.simple_io import load_json
from oolongt.typing.repr_able import ReprAble


def get_config_paths(root, lang):
    # type: (str, str) -> str
    """Get path to language config

    Arguments:
        root {str} -- root directory
        lang {str} -- basename of config

    Returns:
        Path -- pathlib.Path to file
    """
    root_path = Path(root)
    return root_path.joinpath(lang + '.json'), root_path


def get_stop_word_key(stop_cfg, key, nltk_language, default_val=[]):
    # type: (any, str) -> list[str]
    """Get stop words from specified key

    Returns:
        list[str] -- list of stop words
    """
    spec = stop_cfg.get(key, default_val)

    if spec == 'nltk':
        spec = stopwords.words(nltk_language)

    return list(spec)


def get_stop_words(lang_spec, nltk_language, defaults):
    # type: (dict, str) -> set
    """List stop words based on language configuration

    Returns:
        list[str] -- list of stop words
    """
    stop_cfg = defaults.copy()
    stop_cfg.update(lang_spec.get('stop_words', {}))

    initial = get_stop_word_key(
        stop_cfg, 'initial', nltk_language, 'nltk')  # type: list
    custom = get_stop_word_key(
        stop_cfg, 'custom', nltk_language)           # type: list

    return set(initial + custom)


def parse_config(path):
    # type: (str) -> tuple[int, str, list[str]]
    DEFAULT_STOP_WORDS = {
        'initial': DEFAULT_INITIAL_STOPS,
        'custom': DEFAULT_CUSTOM_STOPS, }

    try:
        lang_spec = load_json(path)

        ideal = lang_spec.get(
            'ideal', DEFAULT_IDEAL_LENGTH)                 # type: int
        nltk_language = lang_spec.get(
            'nltk_language', DEFAULT_NLTK_LANGUAGE)        # type: str
        stop_words = get_stop_words(
            lang_spec, nltk_language, DEFAULT_STOP_WORDS)  # type: list[str]

    except (KeyError, JSONDecodeError):
        raise ValueError('invalid config file: {!r}'.format(path))

    return int(ideal), str(nltk_language), list(stop_words)


def load_language(root=BUILTIN, lang=DEFAULT_LANG):
    # type: (str, str) -> tuple[int, str, list[str]]
    """Get class initialization data from `root`/`lang`.json

    Arguments:
        root {str} -- root directory of language data
            (default: {parser.BUILTIN})
        lang {str} -- basename of language file
            (default: {parser.DEFAULT_LANG})

    Raises:
        PermissionError -- Directory traversal via lang
        FileNotFoundError -- Language file(s) not found

    Returns:
        dict -- class initialization data
    """
    cfg_path, root_path = get_config_paths(root, lang)

    try:
        # pylint: disable=no-member
        cfg_path.resolve().relative_to(root_path.resolve())

    except ValueError:
        raise PermissionError('directory traversal in lang: ' + lang)

    # pylint: disable=no-member
    if not cfg_path.exists():
        raise FileNotFoundError(cfg_path)

    config = parse_config(str(cfg_path.absolute()))

    return config


class ParserConfig(ReprAble):
    def __init__(self, root, lang):
        ideal, nltk_language, stop_words = load_language(root, lang)

        self.ideal_sentence_length = ideal  # type: int
        self.nltk_language = nltk_language  # type: str
        self.stop_words = stop_words        # type: list[str]
