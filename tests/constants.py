"""Test constants"""
from pathlib import Path

DATA_PATH = Path(__file__).parent.joinpath('data')
TEXT_PATH = DATA_PATH.joinpath('text')
DOC_PATH = DATA_PATH.joinpath('content')
IDIOM_PATH = DATA_PATH.joinpath('idioms')
SAMPLES = ['cambodia', 'cameroon', 'canada']
