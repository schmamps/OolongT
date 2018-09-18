"""Base class for common tasks"""
import typing  # noqa  pylint: disable=unused-import
from pathlib import Path

from setuptools import Command


# pylint: disable=attribute-defined-outside-init,unnecessary-pass
class OolongtTask(Command):
    """Base class for other setuptools commands"""
    user_options = []  # type: typing.List[tuple]

    def initialize_options(self):
        """initialize options"""
        self.project_root = Path(__file__).parent.parent.parent

    def finalize_options(self):
        """dummy"""
        pass

    def get_project_path(self, *args):
        """Get Path object as subdirectory of project root

        Returns:
            Path -- Path to subdirectory
        """
        return self.project_root.joinpath(*args)
