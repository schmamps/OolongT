"""Setup Script"""
import setuptools

# pylint: disable=no-name-in-module
from setup.cleanup_command import CleanupCommand
from setup.generate_command import GenerateCommand
from setup.nltk_command import NltkCommand
from setup.py_test_command import PyTestCommand

# pylint: enable=no-name-in-module


def readme() -> str:
    """Load README.md

    Returns:
        str -- contents of README
    """
    with open('README.md', 'r') as fp:  # pylint: disable=invalid-name
        return fp.read()


setuptools.setup(
    name='oolongt',
    version='1.100.0',
    author='Andrew Champion',
    author_email='awchampion@gmail.com',
    description='A text summarization library',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/schmamps/OolongT/',
    packages=setuptools.find_packages(where='src', ),
    package_dir={'': 'src', },
    keywords=['summarization', ],
    package_data={'': ['idioms/*.json'], },
    scripts=['bin/oolongt'],
    setup_requires=['pytest-runner', ],
    tests_require=['pytest', ],
    cmdclass={
        'pytest': PyTestCommand,
        'generate': GenerateCommand,
        'nltk': NltkCommand,
        'cleanup': CleanupCommand, },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent', ],
)
