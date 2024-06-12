from nbconvert.preprocessors import Preprocessor

class IgnorePipInstallPreprocessor(Preprocessor):
    def preprocess(self, nb, resources):
        # Filter out cells that contain a pip install command
        nb.cells = [cell for cell in nb.cells if not (cell.cell_type == 'code' and cell.source.startswith('!pip install'))]
        return nb, resources


c = get_config()
c.Exporter.preprocessors = [IgnorePipInstallPreprocessor]

