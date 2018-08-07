import sys


if sys.version_info[0] < 3:
    sys.path.append('..')
    JSONDecodeError = ValueError
    PermissionError = IOError

else:
    from json import JSONDecodeError
    PermissionError = PermissionError
