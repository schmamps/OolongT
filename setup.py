import os

REQUIREMENTS = 'r'
DOWNLOAD = 'd'
QUIT = 'Q'


def get_input(msg, options=['y', 'n'], default='n'):
    display_options = list(options)

    try:
        default_index = options.index(default)
        display_options[default_index] = default.upper()

    except ValueError:
        pass

    prompt = '[' + '/'.join(display_options) + ']'
    val = input(' '.join([msg, prompt]) + '? ')[:1].lower()

    if val in options:
        return val

    print('input: ' + default)

    return default


def prompt_requirements():
    msg = """
To install the requirements, run `pip install -r requirements.txt`
or agree to continue at the next prompt. Continue"""
    if get_input(msg) == 'y':
        os.system('pip install -r requirements.txt')

    return True


def prompt_download():
    msg = """
Additional files are required to support the NLTK requirement.
If you agree to continue, the download interface will appear.
Continue"""
    if get_input(msg) == 'y':
        print('\nlook for the download interface window...\n')

        import nltk
        nltk.download()

    return True


def menu():
    msg = 'Install [r]equirements, download [d]ata, or [q]uit'
    response = get_input(msg, [REQUIREMENTS, DOWNLOAD, QUIT], QUIT)

    if response == QUIT:
        return False

    if response == REQUIREMENTS:
        return prompt_requirements()

    if response == DOWNLOAD:
        return prompt_download()


def main():
    print('\nOolongT Setup' + '-' * 46)

    while menu():
        print('')

    print('')
    quit()


main()
