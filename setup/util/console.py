"""Fancy console functions"""
import typing

from colorama import Fore, Style, init

init()


GROUP_LEVEL = -1


def _print(text: str, *args, fore=None, style=None):
    """Print text (overloaded)

    Arguments:
        text {str} -- text to print

    Keyword Arguments:
        fore {bool} -- foreground color (default: {False})
        style {bool} -- text style (default: {False})
    """
    global GROUP_LEVEL  # pylint: disable=global-statement

    pad = '  ' * GROUP_LEVEL
    fore_color = fore if fore else ''
    para_style = style if style else ''
    reset = Fore.RESET + Style.RESET_ALL

    print('{}{}{}{}{}'.format(
        pad, fore_color, para_style, str(text).format(*args), reset))


def group(text: str = ''):
    """Group console output

    Keyword Arguments:
        text {str} -- group heading (default: {''})
    """
    global GROUP_LEVEL  # pylint: disable=global-statement
    GROUP_LEVEL = max(0, GROUP_LEVEL)

    if text:
        _print(text, style=Style.BRIGHT)

    GROUP_LEVEL += 1


def group_end(text: str = ''):
    """Ungroup console output

    Keyword Arguments:
        text {str} -- end of group text (default: {''})
    """
    global GROUP_LEVEL  # pylint: disable=global-statement
    group(text)

    GROUP_LEVEL -= 2


def get_bullets(ordered: bool, count: int):
    """List bullets for items

    Arguments:
        ordered {bool} -- list style
        count {int} -- number of items

    Returns:
        typing.List[str] -- list of bullets
    """
    if ordered:
        template = '{{:>{}s}}.'.format(len(str(count)))
        return [template.format(str(i + 1)) for i in range(count)]

    return ['*'] * count


def list_items(items: typing.List[typing.Any], *args, ordered=False):
    """Print `items` to console as list

    Arguments:
        items {typing.List[typing.Any]} -- item list

    Keyword Arguments:
        ordered {bool} -- print as ordered list (default: {False})
    """
    count = len(items)
    bullets = get_bullets(ordered, count)

    for idx in range(count):
        _print('{} {}'.format(bullets[idx], items[idx]), *args)


def log(text: typing.Any, *args):
    """Print to console

    Arguments:
        text {typing.Any} -- text
    """
    _print(text, *args)


def info(text: typing.Any, *args):
    """Print to console (muted)

    Arguments:
        text {typing.Any} -- text
    """
    _print(text, *args, style=Style.DIM)


def success(text: typing.Any, *args):
    """Print to console (green)

    Arguments:
        text {typing.Any} -- text
    """
    _print(text, *args, fore=Fore.GREEN)


def warn(text: typing.Any, *args):
    """Print to console (yellow)

    Arguments:
        text {typing.Any} -- text
    """
    _print(text, *args, fore=Fore.YELLOW)


def error(text: typing.Any, *args):
    """Print to console (red)

    Arguments:
        text {typing.Any} -- text
    """
    _print(text, *args, fore=Fore.RED)


# pylint: disable=invalid-name
def lf():
    """Print blank line"""
    _print('')


def ol(items: typing.List[typing.Any], *args):
    """Print ordered list

    Arguments:
        items {typing.List[typing.Any]} -- item list
    """
    list_items(items, *args, ordered=True)


def ul(items: typing.List[typing.Any], *args):
    """Print unordered list

    Arguments:
        items {typing.List[typing.Any]} -- item list
    """
    list_items(items, *args, ordered=False)
