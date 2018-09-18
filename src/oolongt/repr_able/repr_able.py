"""Class REPR helper"""


class ReprAble:
    """Common class methods"""
    def _repr_(self, *args, **kwargs) -> str:
        """Simplify REPR method

        Returns:
            str -- class REPR
        """
        class_name = self.__class__.__name__
        p_args = [repr(v) for v in args]
        k_args = ['{}={!r}'.format(k, v) for k, v in kwargs.items()]

        return '{}({})'.format(class_name, ', '.join(p_args + k_args))

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
