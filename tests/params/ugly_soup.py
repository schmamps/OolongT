"""UglySoup test parameters"""
from src.oolongt.io import load_json, read_file
from src.oolongt.ugly_soup import UglySoup
from tests.constants import DOC_PATH

MARKUP = read_file(DOC_PATH.joinpath('intermed.html'))
SOUP = UglySoup(MARKUP, features='html.parser')
DOC = load_json(DOC_PATH.joinpath('intermed.json'))
