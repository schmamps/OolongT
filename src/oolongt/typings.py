"""Custom type definitions"""
import pathlib  # noqa: F401
import typing

PathOrString = typing.Union[str, pathlib.Path]
OptionalString = typing.Optional[str]
StringList = typing.List[str]
AnyList = typing.List[typing.Any]
OptionalStringList = typing.Union[OptionalString, StringList]
DictOfAny = typing.Dict[str, typing.Any]
DictOfFloat = typing.Dict[str, float]
