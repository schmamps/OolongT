class ReprAble:
    def _repr_(self, *args):
        template = '{0}({1})'.format(
            self.__class__.__name__, ', '.join(['{!r}'] * len(args)))

        return template.format(*args)