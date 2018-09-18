"""Setup Script"""
import typing

import setuptools

# pylint: disable=no-name-in-module
from src.oolongt.constants import VERSION
from src.setup.cleanup_command import CleanupCommand
from src.setup.generate_command import GenerateCommand
from src.setup.nltk_command import NltkCommand
from src.setup.py_test_command import PyTestCommand


# pylint: enable=no-name-in-module
def load_file(path) -> typing.List[str]:
    with open(path, 'r') as stream:
        lines = [line.strip() for line in stream.readlines()]

    return [line for line in lines if line]


ALL_REQS = load_file('src/oolongt/requirements.txt')
DEP_LINKS = [req for req in ALL_REQS if req.startswith('git+')]


setuptools.setup(
    name='oolongt',
    version=VERSION,
    author='Andrew Champion',
    author_email='awchampion@gmail.com',
    description='A text summarization library',
    long_description='\n'.join(load_file('README.md')),
    long_description_content_type='text/markdown',
    url='https://github.com/schmamps/OolongT/',
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    keywords=['summarization'],
    package_data={'': ['idioms/*.json']},
    scripts=['bin/oolongt'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    cmdclass={
        'pytest': PyTestCommand,
        'generate': GenerateCommand,
        'nltk': NltkCommand,
        'cleanup': CleanupCommand,
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        req for req in ALL_REQS if req not in DEP_LINKS
    ],
    dependency_links=[req[4:] for req in DEP_LINKS],
)
