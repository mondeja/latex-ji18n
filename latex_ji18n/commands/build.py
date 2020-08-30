import inspect
import os

from latex_ji18n.context import LanguageContext, ProjectContext
from latex_ji18n.environment import LatexJinja2Environment
from latex_ji18n.executable import PdfLatexExecutable
from latex_ji18n.filters import DEFAULT_FILTERS
from latex_ji18n.render import LatexJinja2Renderer


def run(
    languages=None,
    project_path=None,
    environment=LatexJinja2Environment,
    filters=DEFAULT_FILTERS,
    executable=PdfLatexExecutable,
):
    if not project_path:
        project_path = os.getcwd()
    if inspect.isclass(executable):
        executable = executable()

    renderer = LatexJinja2Renderer(environment=environment, filters=filters)
    project_context = ProjectContext(project_path=project_path)
    project_context._prepare()
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
        renderer.render(
            template_filepath,
            context=language_context,
            destpath=language_context.localized_tex_filepath,
        )

        # Compile with Latex
        with project_context.sourcedir_as_cwd():
            executable.run(language_context.localized_tex_filename)

        expected_filename = "%s%s" % (language, executable.output_extension)
        expected_filepath = os.path.join(
            project_context.source_dirpath, expected_filename
        )
        if not os.path.exists(expected_filepath):
            break

        dist_filepath = os.path.join(project_context.dist_dirpath, expected_filename)
        os.rename(expected_filepath, dist_filepath)
