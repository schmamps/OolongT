"""Generate test data"""
from .generate import keywords, merge, sentences  # noqa
from .oolongt_task import OolongtTask

OUTPUT_DIR = 'generated_data'


class GenerateCommand(OolongtTask):
    """Data generation command"""
    def run(self):
        """Generate test data"""
        self.announce('generating test data', level=2)

        input_dir = self.get_project_path('tests', 'data', 'text')
        output_dir = self.get_project_path(OUTPUT_DIR)

        for module in [keywords, sentences, merge]:
            module.generate(input_dir, output_dir)
