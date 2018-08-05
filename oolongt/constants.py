from pathlib import Path

# summarizer
DEFAULT_LENGTH = 5

# approximation
DEFAULT_TOLERANCE = 0.0000001  # simple floats
COMPOSITE_TOLERANCE = 0.00000011   # composite scores

# parser
BUILTIN = Path(__file__).parent.joinpath('lang')
DEFAULT_LANG = 'en'
DEFAULT_IDEAL_LENGTH = 20
DEFAULT_NLTK_LANGUAGE = 'english'
DEFAULT_NLTK_STOPS = True
DEFAULT_USER_STOPS = []

# scored keyword
KEYWORD_SCORE_K = 1.5
