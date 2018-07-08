"""Compare floating point values"""
DEFAULT_TOLERANCE = 0.0000001


def eq(a, b, rel_tol=DEFAULT_TOLERANCE, abs_tol=0.0):
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
    # type: (float, float, float, float) -> bool
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def ne(a, b, rel_tol=DEFAULT_TOLERANCE, abs_tol=0.0):
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
    # type: (float, float, float, float) -> bool
    return not eq(a, b, rel_tol, abs_tol)


def lt(a, b, rel_tol=DEFAULT_TOLERANCE, abs_tol=0.0):
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
    # type: (float, float, float, float) -> bool
    return a < b and not eq(a, b, rel_tol, abs_tol)


def gt(a, b, rel_tol=DEFAULT_TOLERANCE, abs_tol=0.0):
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
    # type: (float, float, float, float) -> bool
    return a > b and not eq(a, b, rel_tol, abs_tol)


def ge(a, b, rel_tol=DEFAULT_TOLERANCE, abs_tol=0.0):
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
    # type: (float, float, float, float) -> bool
    return not lt(a, b, rel_tol, abs_tol)


def le(a, b, rel_tol=DEFAULT_TOLERANCE, abs_tol=0.0):
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
    # type: (float, float, float, float) -> bool
    return not gt(a, b, rel_tol, abs_tol)
