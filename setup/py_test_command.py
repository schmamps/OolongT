"""Run pytest"""
import sys

from setuptools.command.test import test as TestCommand


# pylint: disable=attribute-defined-outside-init,unnecessary-pass
class PyTestCommand(TestCommand):
    """Test command"""
    user_options = [('pytest-args=', 'a', 'Arguments to pass to pytest')]

    def initialize_options(self):
        """initialize options"""
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        """run pytest"""
        import shlex

        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)
