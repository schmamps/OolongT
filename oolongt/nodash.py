""" lodash-like functionality """


def pluck(iterable, key):
    # type: (list, any) -> list[any]
    """Get value at `key` in iterable of Dicts

    Arguments:
        iterable {iterable} -- an iterable of Dicts
        key {any} -- key in each dict to extract

    Returns:
        list[any] -- all values at specified key
    """
    return [item[key] for item in iterable]


def get_sort_tuple(item, key):
    # type: (dict, any) -> tuple
    """Create tuple of values suitable for sorted()

    Arguments:
        item {dict} -- Dict to be sorted
        key {any} -- sorting criteria, descending order

    Returns:
        tuple -- value(s) for sorting
    """
    values = [item[k] for k in key] if isinstance(key, list) else [item[key]]

    return tuple(values)


def sort_by(iterable, key, reverse=False):
    # type: (list, any, bool) -> list[any]
    """Sort `iterable` of Dicts by one or more `key`s

    Arguments:
        iterable {iterable} -- iterable list of Dicts
        key {any or list[any]} -- key(s) to use for sort

    Keyword Arguments:
        reverse {bool} -- False: ASC, True: DESC (default: {False})

    Returns:
        list[any] -- sorted iterable
    """
    return sorted(
        iterable, key=lambda x: get_sort_tuple(x, key), reverse=reverse)
