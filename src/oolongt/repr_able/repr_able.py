"""Class REPR helper"""


class ReprAble:
    """Common class methods"""
    def _repr_(self, *args, **kwargs) -> str:
        """Simplify REPR method

        Returns:
            str -- class REPR
        """
        all_args = ', '.join(
            [repr(val) for val in args]
            +
            [f'{key}={repr(val)}' for key, val in kwargs.items()]
        )

        return f'{self.__class__.__name__}({all_args})'

    def __lt__(self, other) -> bool:
        return str(self) < str(other)

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    def __gt__(self, other) -> bool:
        return str(self) > str(other)

    def __ne__(self, other) -> bool:
        return not self == other

    def __ge__(self, other) -> bool:
        return not self < other

    def __le__(self, other) -> bool:
        return not self > other
