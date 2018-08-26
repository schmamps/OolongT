"""Cleanup project directory"""
from os.path import exists
from shutil import rmtree

from .generate_command import OUTPUT_DIR
from .oolongt_task import OolongtTask


class CleanupCommand(OolongtTask):
    def run(self):
        """Delete intermediate folders"""
        self.announce('deleting intermediate folders', level=2)

        for sub in [OUTPUT_DIR, 'build', 'dist']:
            path = self.get_project_path(sub)
            level = 2
            glyph = '√'

            try:
                if exists(path):
                    rmtree(path)

            except OSError:
                level = 4
                glyph = '!'

            self.announce('{:14s}: {}'.format(path.stem, glyph), level=level)
