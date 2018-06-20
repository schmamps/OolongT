""" lodash-like functionality """


def pluck(iterable, key):
    """Get value at specified key in a list of Dicts

    Arguments:
        iterable {iterable} -- an iterable of Dicts
        key {any} -- key in each dict to extract

    Returns:
        list[any] -- all values at specified key
    """
    return [item[key] for item in iterable]


def get_sort_tuple(item, key):
    """Create tuple of values suitable for sorted()

    Arguments:
        item {Dict} -- Dict to be sorted
        key {any, List[any]} -- sorting criteria, descending order

    Returns:
        any -- value(s) for sorting
    """
    if isinstance(key, list):
        values = [item[x] for x in key]

        return tuple(values)

    return item[key]


def sort_by(iterable, key, reverse=False):
    """Sort iterable of Dicts using value of one or more keys

    Arguments:
        iterable {iterable} -- iterable list of Dicts
        key {any or List[any]} -- key(s) to use for sort

    Keyword Arguments:
        reverse {bool} -- False: ASC, True: DESC (default: {False})

    Returns:
        List[any] -- sorted iterable
    """
    return sorted(
        iterable, key=lambda x: get_sort_tuple(x, key), reverse=reverse)
