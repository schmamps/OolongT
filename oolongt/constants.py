from typing import List
from pathlib import Path

# summarizer
DEFAULT_LENGTH = 5
TOP_KEYWORD_MIN_RANK = 10

# approximation
DEFAULT_TOLERANCE = 0.0000000001    # simple floats
COMPOSITE_TOLERANCE = 0.0000000001  # composite scores

# parser
BUILTIN = str(Path(__file__).parent.joinpath('lang'))
DEFAULT_LANG = 'en'
DEFAULT_IDEAL_LENGTH = 20
DEFAULT_NLTK_LANGUAGE = 'english'
DEFAULT_NLTK_STOPS = True
DEFAULT_USER_STOPS = []   # type: List[str]

# scored keyword
KEYWORD_SCORE_K = 1.5
