def pluck(iterable, key):
    return [item[key] for item in iterable]


def sort_by(iterable, keyName, reverse=False):
    return sorted(iterable, key=lambda x: x[keyName], reverse=reverse)
