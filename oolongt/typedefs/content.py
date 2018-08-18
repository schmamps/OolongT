import re
from pathlib import Path
from typing import Callable
from unicodedata import normalize

from oolongt.typedefs.repr_able import ReprAble


def create_title(path: str) -> str:
    file_path = Path(path)

    stem = normalize(
        'NFKD', file_path.stem).encode('ascii', 'ignore').decode('utf8')
    words = re.split(r'[,_\-\.\s]+', stem, flags=re.IGNORECASE)

    return ' '.join(words).title()


class Content(ReprAble):
    def __init__(self, load_func: Callable, path: str, catch=OSError) -> None:
        try:
            body_spec, title_spec, keywords = load_func(path)
        except Exception as e:
            if not isinstance(e, catch):
                raise e

            raise ValueError('Cannot load {!r} as content'.format(path))

        self.load_func = load_func.__name__
        self.title_spec = title_spec
        self.path = path
        self.body = body_spec or ''
        self.title = title_spec or create_title(path)

    def __repr__(self):
        return self._repr_(self.path, self.body, self.title_spec)

    def __str__(self):
        return self.body
