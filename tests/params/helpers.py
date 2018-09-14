"""Parametrizing helpers"""
import typing

from pytest import mark

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


def parametrize(
        names: str,
        vals: typing.List,
        ids: typing.List[str]):
    """Simplify `pytest.mark.parametrize`

    Arguments:
        names {str} -- parameter names
        vals {typing.Iterable} -- parameter values
        ids {StringList} -- test IDs
    """
    return mark.parametrize(names, list(vals), ids=pad_to_longest(list(ids)))
