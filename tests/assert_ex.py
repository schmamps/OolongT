""" Assertion Helpers """
import doctest


def compare_list(left, right):
    """Compare left to right, generate diff

    Arguments:
        left {List[Any]} - reference list
        right {List[Any]} - list to compare against

    Returns:
        str -- comparison of left to right

    >>> compare_list([1, 2, 3], [2, 3, 4])
    'len: 3, exclusive: [1]'
    >>> compare_list([1, 2, 3], [1, 2, 3, 4])
    'len: 3, exclusive: []'
    """
    len_str = 'len: ' + str(len(left))
    diff_str = 'exclusive: ' + str([x for x in left if x not in right])

    return ', '.join([len_str, diff_str])


def assert_ex(msg, result, expected, **kwargs):
    """Generate detailed AssertionError exceptions

    Arguments:
        msg {str} -- description of error
        result {any} -- outcome of test
        expected {any} -- expected outcome of test

    Returns:
        bool -- tested condition

    >>> rv = [0]
    >>> ev = [0]
    >>> assert_ex('Error', rv, ev)
    True
    >>> rv = [0]
    >>> ev = [1]
    >>> assert_ex('Mismatch', rv, ev)
    Traceback (most recent call last):
    ...
    AssertionError: Mismatch
    result   > len: 1, exclusive: [0]
    expected > len: 1, exclusive: [1]
    >>> rv = [0]
    >>> rc = len(rv)
    >>> ev = [1]
    >>> ec = len(ev)
    >>> assert_ex('Length', rv, ev, test=rc == ec)
    True
    >>> rv = int(1)
    >>> rc = len(str(rv))
    >>> ev = float(1)
    >>> ec = len(str(ev))
    >>> assert_ex('Precision', rv, ev, test=(rc == ec))
    Traceback (most recent call last):
    ...
    AssertionError: Precision
    result   > 1
    expected > 1.0
    >>> rv = int(1)
    >>> rc = len(str(rv))
    >>> ev = float(1)
    >>> ec = len(str(ev))
    >>> assert_ex('Precision', rv, ev, test=(rc == ec), hint='places')
    Traceback (most recent call last):
    ...
    AssertionError: Precision ('places')
    result   > 1
    expected > 1.0
    """
    test = None
    hint = ''

    for key, val in kwargs.items():
        if key == 'test':
            test = val
            continue

        if key == 'hint':
            hint = ' (' + repr(val) + ')'
            continue

    if test is None:
        test = (result == expected)

    if test:
        return test

    res_str = str(result)
    exp_str = str(expected)

    if isinstance(result, list) and isinstance(expected, list):
        res_str = compare_list(result, expected)
        exp_str = compare_list(expected, result)

    assert test, '\n'.join([
        msg + hint, 'result   > ' + res_str, 'expected > ' + exp_str])

    return test
