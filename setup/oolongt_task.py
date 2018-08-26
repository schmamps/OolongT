"""Base class for common tasks"""
import typing  # noqa
from pathlib import Path
from setuptools import Command


class OolongtTask(Command):
    user_options = []  # type: typing.List[tuple]

    def initialize_options(self):
        self.project_root = Path(__file__).parent.parent
        pass

    def finalize_options(self):
        pass

    def get_project_path(self, *args):
        """Get Path object as subdirectory of project root

        Returns:
            Path -- Path to subdirectory
        """
        return self.project_root.joinpath(*args)
