import sys


if sys.version_info[0] < 3:
    sys.path.append('..')
    PermissionError = IOError
    FileNotFoundError = IOError
    JSONDecodeError = ValueError

else:
    PermissionError = PermissionError
    FileNotFoundError = FileNotFoundError  # pylint: disable=undefined-variable
    from json import JSONDecodeError       # pylint: disable=no-name-in-module
