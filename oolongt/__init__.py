import sys


PYTHON_2 = (sys.version_info[0] < 3)


if PYTHON_2:
    sys.path.append('..')


from oolongt.main import summarize, score_body_sentences  # noqa
