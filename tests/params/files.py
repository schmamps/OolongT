from src.oolongt.io import load_json
from tests.constants import DOC_PATH


def get_doc_path(stem: str, ext: str = 'html'):
    return DOC_PATH.joinpath('{}.{}'.format(stem, ext))


def get_doc(stem: str):
    path = str(get_doc_path(stem, 'json'))
    data = load_json(path)

    return data['body'], data['title']


BASIC_BODY, BASIC_TITLE = get_doc('basic')
INTERMED_BODY, INTERMED_TITLE = get_doc('intermed')

TEST_PATH = '/spam/eggs/bacon.ham'
