"""Custom type definitions"""
import pathlib  # noqa: F401
import typing  # noqa: F401

PathOrString = typing.Union[str, pathlib.Path]
OptionalString = typing.Optional[str]
StringList = typing.List[str]
OptionalStringList = typing.Union[OptionalString, StringList]
DictOfAny = typing.Dict[str, typing.Any]
DictOfFloat = typing.Dict[str, float]
