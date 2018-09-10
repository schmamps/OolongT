"""Package Constants"""
# pylint: disable=unused-import
from pathlib import Path
from typing import List  # noqa: F401


# versioning
PKG_NAME = 'OolongT'
VERSION_MAJOR = 1
VERSION_MINOR = 100
VERSION_REV = 0
VERSION = '{}.{}.{}'.format(VERSION_MAJOR, VERSION_MINOR, VERSION_REV)

# summarizer
DEFAULT_LENGTH = 5
TOP_KEYWORD_MIN_RANK = 10

# approximation
COMPOSITE_TOLERANCE = 0.000000000001  # composite scores

# parser
# mypy needs this hint for some reason...
BUILTIN = str(Path(__file__).parent.joinpath('idioms'))  # type: str
DEFAULT_IDIOM = 'default'
DEFAULT_IDEAL_LENGTH = 20
DEFAULT_LANGUAGE = 'english'
DEFAULT_NLTK_STOPS = True
DEFAULT_USER_STOPS = []   # type: List[str]

# scored keyword
KEYWORD_SCORE_K = 1.5
