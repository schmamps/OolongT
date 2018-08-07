import sys


if sys.version_info[0] < 3:
    sys.path.append('..')


from oolongt.main import summarize, score_body_sentences  # nopep8
