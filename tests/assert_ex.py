""" Assertion Helpers """
import doctest


def compare_list(left, right):
    """Compare left to right, generate diff

    Arguments:
        left {List[Any]} - reference list
        right {List[Any]} - list to compare against

    Returns:
        str -- length of left list, REPR of exclusive values

    >>> compare_list([1, 2, 3], [2, 3, 4])
    "len: 3, exclusive: ['1']"
    >>> compare_list([1, 2, 3], [1, 2, 3, 4])
    'len: 3, exclusive: []'
    """
    len_str = 'len: ' + str(len(left))
    diff_str = 'exclusive: ' + str([repr(x) for x in left if x not in right])

    return ', '.join([len_str, diff_str])


# noqa
def assert_ex(msg, result, expected, hint=None):
    """Generate detailed AssertionError exceptions

    Arguments:
        msg {str} -- description of error
        result {any} -- outcome of test
        expected {any} -- expected outcome of test

    Returns:
        bool -- tested condition

    >>> rv = [0]
    >>> ev = [1]
    >>> assert_ex('Mismatch', rv, ev)[:63]
    "Mismatch\\nresult   > len: 1, exclusive: ['0']\\nexpected > len: 1,"
    >>> rv = int(1)
    >>> rc = len(str(rv))
    >>> ev = float(1)
    >>> ec = len(str(ev))
    >>> assert_ex('Precision', rv, ev, hint='float')
    "Precision ('float')\\nresult   > 1\\nexpected > 1.0"
    """
    if hint is not None:
        hint = ' (' + repr(hint) + ')'
    else:
        hint = ''

    res_str = str(result)
    exp_str = str(expected)

    if isinstance(result, list) and isinstance(expected, list):
        res_str = compare_list(result, expected)
        exp_str = compare_list(expected, result)

    return '\n'.join([
        msg + hint,
        'result   > ' + res_str,
        'expected > ' + exp_str])
