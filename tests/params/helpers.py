"""Parametrizing helpers"""
import typing

from pytest import mark

from src.oolongt import it
from src.oolongt.typings import AnyList, StringList


def pad_to_longest(vals: AnyList) -> StringList:
    """Pad all strings to length of longest in list

    Arguments:
        strs {StringList} -- string list

    Returns:
        StringList -- list of strings
    """
    strs = [str(x) for x in vals]
    pad_len = max([len(x) for x in strs])
    pad_str = ' ' * pad_len
    padded = [(x + pad_str)[:pad_len] for x in strs]

    return padded


def check_parametrize(vals, ids: typing.Sequence) -> bool:
    """Try to prevent bad parameters parametrization

    Arguments:
        vals {typing.Any} -- values passed to test
        ids {typing.Sequence} -- test IDs

    Returns:
        bool -- params are (probably) OK
    """
    if not isinstance(vals, (tuple, list, set)):
        return True

    val_list = list(vals)  # type: typing.List[typing.List[str]]

    if len(val_list) != len(ids):
        return False

    try:
        if it.erable(val_list[0]):
            counts = [len(val) for val in val_list]

            return min(counts) == max(counts)

    except Exception:  # pylint: disable=broad-except
        pass

    return True


def parametrize(
        names: str,
        vals: typing.Sequence,
        ids: typing.Sequence[str]):
    """Simplify `pytest.mark.parametrize`

    Arguments:
        names {str} -- parameter names
        vals {typing.Iterable} -- parameter values
        ids {StringList} -- test IDs
    """
    if not check_parametrize(vals, ids):
        breakpoint()

    return mark.parametrize(names, list(vals), ids=pad_to_longest(list(ids)))
