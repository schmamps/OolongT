"""Compare floating point values"""
from oolongt.constants import DEFAULT_TOLERANCE


def eq(
        a: float,
        b: float,
        rel_tol: float = DEFAULT_TOLERANCE,
        abs_tol: float = 0.0
        ) -> bool:
    """Test `a`(-ish) == `b`(-ish)

    Arguments:
        a {float} -- value
        b {float} -- another value

    Keyword Arguments:
        rel_tol {float} -- relative tolerance (default: {DEFAULT_TOLERANCE})
        abs_tol {float} -- absolute tolerance (default: {0.0})

    Returns:
        bool -- equivalent
    """
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def ne(
        a: float,
        b: float,
        rel_tol: float = DEFAULT_TOLERANCE,
        abs_tol: float = 0.0
        ) -> bool:
    """Test `a`(-ish) != `b`(-ish)

    Arguments:
        a {float} -- value
        b {float} -- another value

    Keyword Arguments:
        rel_tol {float} -- relative tolerance (default: {DEFAULT_TOLERANCE})
        abs_tol {float} -- absolute tolerance (default: {0.0})

    Returns:
        bool -- not equivalent
    """
    return not eq(a, b, rel_tol, abs_tol)


def lt(
        a: float,
        b: float,
        rel_tol: float = DEFAULT_TOLERANCE,
        abs_tol: float = 0.0
        ) -> bool:
    """Test `a`(-ish) < `b`(-ish)

    Arguments:
        a {float} -- value
        b {float} -- another value

    Keyword Arguments:
        rel_tol {float} -- relative tolerance (default: {DEFAULT_TOLERANCE})
        abs_tol {float} -- absolute tolerance (default: {0.0})

    Returns:
        bool -- `a` is less than `b`
    """
    return a < b and not eq(a, b, rel_tol, abs_tol)


def gt(
        a: float,
        b: float,
        rel_tol: float = DEFAULT_TOLERANCE,
        abs_tol: float = 0.0
        ) -> bool:
    """Test `a`(-ish) > `b`(-ish)

    Arguments:
        a {float} -- value
        b {float} -- another value

    Keyword Arguments:
        rel_tol {float} -- relative tolerance (default: {DEFAULT_TOLERANCE})
        abs_tol {float} -- absolute tolerance (default: {0.0})

    Returns:
        bool -- `a` is greater than `b`
    """
    return a > b and not eq(a, b, rel_tol, abs_tol)


def ge(
        a: float,
        b: float,
        rel_tol: float = DEFAULT_TOLERANCE,
        abs_tol: float = 0.0
        ) -> bool:
    """Test `a`(-ish) >= `b`(-ish)

    Arguments:
        a {float} -- value
        b {float} -- another value

    Keyword Arguments:
        rel_tol {float} -- relative tolerance (default: {DEFAULT_TOLERANCE})
        abs_tol {float} -- absolute tolerance (default: {0.0})

    Returns:
        bool -- `a` is greater than/equal to `b`
    """
    return not lt(a, b, rel_tol, abs_tol)


def le(
        a: float,
        b: float,
        rel_tol: float = DEFAULT_TOLERANCE,
        abs_tol: float = 0.0
        ) -> bool:
    """Test `a`(-ish) <= `b`(-ish)

    Arguments:
        a {float} -- value
        b {float} -- another value

    Keyword Arguments:
        rel_tol {float} -- relative tolerance (default: {DEFAULT_TOLERANCE})
        abs_tol {float} -- absolute tolerance (default: {0.0})

    Returns:
        bool -- `a` is less than/equal to `b`
    """
    return not gt(a, b, rel_tol, abs_tol)
