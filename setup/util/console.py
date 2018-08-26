from colorama import Fore, Style, init

init()


GROUP_LEVEL = -1


def _print(text, *args, fore=False, style=False):
    global GROUP_LEVEL

    pad = '  ' * GROUP_LEVEL
    fore_color = fore if fore else ''
    para_style = style if style else ''
    reset = Fore.RESET + Style.RESET_ALL

    print('{}{}{}{}{}'.format(
        pad, fore_color, para_style, str(text).format(*args), reset))


def group(text='', *args):
    global GROUP_LEVEL
    GROUP_LEVEL = max(0, GROUP_LEVEL)

    if text:
        _print(text, *args, style=Style.BRIGHT)

    GROUP_LEVEL += 1


def group_end(text=''):
    global GROUP_LEVEL
    group(text)

    GROUP_LEVEL -= 2


def _format_ordered_bullet(idx, tick_pad):
    padded = (' ' * tick_pad) + str(idx + 1) + '.'

    return padded[-tick_pad - 1:]


def get_bullets(ordered, count):
    if ordered:
        tick_pad = len(str(count))
        return [_format_ordered_bullet(i, tick_pad) for i in range(count)]

    else:
        return ['*'] * count


def list_items(items, ordered=False):
    count = len(items)
    bullets = get_bullets(ordered, count)

    for idx in range(count):
        _print('{} {}'.format(bullets[idx], items[idx]))


def log(text, *args):
    _print(text, *args)


def info(text, *args):
    _print(text, *args, style=Style.DIM)


def success(text, *args):
    _print(text, *args, fore=Fore.GREEN)


def warn(text, *args):
    _print(text, *args, fore=Fore.YELLOW)


def error(text, *args):
    _print(text, *args, fore=Fore.RED)


def lf():
    _print('')


def ol(items, *args):
    list_items(items, *args, ordered=True)


def ul(items, *args):
    list_items(items, *args, ordered=False)
