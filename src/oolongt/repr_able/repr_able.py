"""Class REPR helper"""
import typing


class ReprAble:
    def _un_kwarg(self, kwargs: typing.Dict[str, typing.Any]) -> str:
        if len(kwargs) == 0:
            return ''

        return ', ' + ', '.join([
            '{}={!r}'.format(key, val)
            for key, val in kwargs.items()])

    def _repr_(self, *args, **kwargs) -> str:
        template = '{0}({1}{2})'.format(
            self.__class__.__name__,
            ', '.join(['{!r}'] * len(args)),
            self._un_kwarg(kwargs))

        return template.format(*args)
