import inspect
import os

from jinja2 import FileSystemLoader

from latex_ji18n.build import PdfLatexBuilder
from latex_ji18n.context import LanguageContext, ProjectContext
from latex_ji18n.environment import LatexJinja2Environment
from latex_ji18n.filters import DEFAULT_FILTERS


class LaTeXJi18nRenderer:
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


def render(
    filepath=None,
    languages=None,
    project_path=None,
    environment=LatexJinja2Environment,
    filters=DEFAULT_FILTERS,
    builder=PdfLatexBuilder,
):
    if not project_path:
        project_path = os.getcwd()
    if inspect.isclass(builder):
        builder = builder()

    renderer = LaTeXJi18nRenderer(environment=environment, filters=filters)
    project_context = ProjectContext(project_path=project_path)
    project_context._prepare()
    if filepath is None:
        template_filepath = project_context.template_filepath

    if languages is None:
        languages = project_context.discover_languages()
    for language in languages:
        # Load context
        language_context = LanguageContext(
            language=language, project_context=project_context
        )
        language_context.load()

        # Render template to localized output
        localized_tex_filepath = os.path.join(
            project_context.source_dirpath, language_context.localized_template_name
        )
        localized_tex_filename = os.path.basename(localized_tex_filepath)
        renderer.render(
            template_filepath, context=language_context, destpath=localized_tex_filepath
        )

        # Compile with Latex
        with project_context.sourcedir_as_cwd():
            builder.build(localized_tex_filename)

        expected_filename = "%s.pdf" % language
        expected_filepath = os.path.join(
            project_context.source_dirpath, expected_filename
        )
        if not os.path.exists(expected_filepath):
            break

        dist_filepath = os.path.join(project_context.dist_dirpath, expected_filename)
        os.rename(expected_filepath, dist_filepath)
