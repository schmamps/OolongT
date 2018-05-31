from pathlib import Path

from oolongt import simple_io, summarize

EXIT_RESPONSE = 'q'
READ_RESPONSE = 'r'
SUMM_RESPONSE = 's'


def get_input():
    valid_responses = [EXIT_RESPONSE, READ_RESPONSE, SUMM_RESPONSE]

    try:
        response = input('[s]ummarize, [r]ead, or [q]uit (default: s) > ')
        response = response.lower()

        if response.lower() not in valid_responses:
            raise IndexError()

    except (EOFError, KeyboardInterrupt):
        response = EXIT_RESPONSE
    except IndexError:
        response = SUMM_RESPONSE

    if response == READ_RESPONSE:
        return get_content()
    elif response == SUMM_RESPONSE:
        return get_summary()
    else:
        return False


def get_sample():
    base = str(Path(__file__).parent.joinpath(
        'tests', 'data', 'essay-snark.'))

    title = simple_io.load_json(base + 'json')['title']
    content = simple_io.read_file(base + 'txt')

    return title, content


def output(desc, title, text):
    print('\n\n'.join([
        '# ' + desc,
        '## ' + title.upper(),
        text]))
    print('\n')

    return True


def get_summary():
    title, content = get_sample()
    length = input(
        '# sentences (float, default: 5, [0 < range < Infinity]) > ')

    try:
        length = float(length)
    except ValueError:
        length = 5

    sentences = summarize(title, content, length=length)
    pad = int(len(sentences) / 10.0)

    text = ''
    for i, sent in enumerate(sentences):
        text += str(i + 1).rjust(pad) + '. ' + sent + '\n'

    return output('SUMMARY', title, text)


def get_content():
    title, text = get_sample()

    return output('CONTENT', title, text)


def main():
    pad = '=' * 30
    print(pad + ' OolongT Demo ' + pad)

    while get_input():
        pass


main()
