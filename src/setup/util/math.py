"""Math functions"""
import typing


def mean(vals: typing.List[float]) -> float:
    """Calculate mean value of `vals`

    Arguments:
        vals {typing.ANy} -- list of values

    Returns:
        float -- mean value
    """
    value_sum = sum([float(val) for val in vals])
    count = len(vals)

    return value_sum / count


def median(vals: typing.List[float]) -> float:
    """Calculate median value of `vals`

    Arguments:
        vals {typing.List[float]} -- list of values

    Returns:
        float -- median value
    """
    index = int(len(vals) / 2) - 1

    return sorted(vals)[index]
