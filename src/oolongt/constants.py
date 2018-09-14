"""Package Constants"""
from pathlib import Path

# pylint: disable=unused-import
from .typings import StringList  # noqa: F401

# pylint: enable=unused-import

# versioning
PKG_NAME = 'OolongT'
VERSION_MAJOR = 1
VERSION_MINOR = 100
VERSION_REV = 0
VERSION = '{}.{}.{}'.format(VERSION_MAJOR, VERSION_MINOR, VERSION_REV)

# summarizer
DEFAULT_LENGTH = 5
TOP_KEYWORD_MIN_RANK = 10
SENTENCE_SCORE_K = 5.0

# approximation
COMPOSITE_TOLERANCE = 0.000000000001  # composite scores

# parser settings
BUILTIN = str(Path(__file__).parent.joinpath('idioms'))
DEFAULT_IDIOM = 'default'
DEFAULT_IDEAL_LENGTH = 20
DEFAULT_LANGUAGE = 'english'
DEFAULT_NLTK_STOPS = True
DEFAULT_USER_STOPS = []   # type: StringList
KEYWORD_SCORE_K = 1.5
