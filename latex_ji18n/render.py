import inspect
import os

from jinja2 import FileSystemLoader

from latex_ji18n.environment import LatexJinja2Environment
from latex_ji18n.filters import DEFAULT_FILTERS


class LatexJinja2Renderer:
    def __init__(self, environment=LatexJinja2Environment, filters=DEFAULT_FILTERS):
        self.environment = environment
        if inspect.isclass(environment):
            self.environment = self.environment()
        self.environment.filters.update(filters)

    def render(self, filepath, context={}, destpath=None):
        filedir = os.path.abspath(os.path.dirname(filepath))
        filename = os.path.basename(filepath)
        self.environment.loader = FileSystemLoader(searchpath=filedir)
        template = self.environment.get_template(filename)
        output = template.render(**context)
        if destpath:
            with open(destpath, "w", encoding="utf-8") as f:
                f.write(output)
        return output
