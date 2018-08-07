"""Parser Configuration Reader"""
from pathlib import Path

from nltk.corpus import stopwords

from oolongt.constants import (BUILTIN, DEFAULT_IDEAL_LENGTH, DEFAULT_LANG,
                               DEFAULT_NLTK_LANGUAGE, DEFAULT_NLTK_STOPS,
                               DEFAULT_USER_STOPS)
from oolongt.simple_io import load_json
from oolongt.typing.repr_able import ReprAble

from oolongt.typing import FileNotFoundError, JSONDecodeError, PermissionError


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


def get_stop_words(lang_spec, nltk_language):
    # type: (dict, str) -> set
    """List stop words based on language configuration

    Returns:
        list[str] -- list of stop words
    """
    stop_cfg = {'nltk': DEFAULT_NLTK_STOPS, 'user': DEFAULT_USER_STOPS, }
    stop_cfg.update(lang_spec.get('stop_words', {}))
    use_nltk = bool(stop_cfg['nltk'])
    use_user = isinstance(stop_cfg['user'], list)

    nltk = stopwords.words(nltk_language) if use_nltk else []
    user = [str(word) for word in stop_cfg['user']] if use_user else []

    return set(nltk + user)


def parse_config(path):
    # type: (str) -> tuple[int, str, list[str]]
    try:
        lang_spec = load_json(path)

        ideal = lang_spec.get(
            'ideal', DEFAULT_IDEAL_LENGTH)           # type: int
        nltk_language = lang_spec.get(
            'nltk_language', DEFAULT_NLTK_LANGUAGE)  # type: str
        stop_words = get_stop_words(
            lang_spec, nltk_language)                # type: list[str]

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

    except (ValueError, OSError):
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
