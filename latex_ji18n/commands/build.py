"""Build a project using custom commands. A set of commands is
called a commands pipe, for example `pdflatex && bibtex && pdflatex`.
If a command in the PIPE fails, the execution is stopped.

Can be built using different commands pipes. If the latest command
in the pipe is `pdflatex`, will be ran
until the `.aux` file doesn't change, specifing a maximum times
that the execution will be repeated until a failure is raised.
"""

import os
import sys

from latex_ji18n.context import LanguageContext, ProjectContext
from latex_ji18n.environment import LatexJinja2Environment
from latex_ji18n.executable import executables
from latex_ji18n.filters import DEFAULT_FILTERS
from latex_ji18n.io import file_md5
from latex_ji18n.render import LatexJinja2Renderer


def run(
    languages=None,
    project_path=None,
    environment=LatexJinja2Environment,
    filters=DEFAULT_FILTERS,
    commands=["pdflatex"],
    max_runs=4,
):
    if not project_path:
        project_path = os.getcwd()

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
        aux_filename = '%s.aux' % language

        with project_context.sourcedir_as_cwd():
            _latest_aux_md5 = None
            if os.path.exists(aux_filename):
                _latest_aux_md5 = file_md5(aux_filename)

            for command in commands:
                if command not in executables:
                    raise ValueError(
                        '\'%s\' command is not a valid latex-ji18n executable' %
                        command)
                exec_arg = (language_context.localized_tex_filename
                            if command == 'pdflatex' else language)
                returncode = executables[command]().run(exec_arg)
                if returncode != 0:
                    sys.exit(returncode)
            if commands[-1] == 'pdflatex':
                aux_md5 = file_md5(aux_filename)
                if aux_md5 != _latest_aux_md5:
                    _latest_aux_md5 = aux_md5
                    n_runs = 0
                    for command in reversed(commands):
                        n_runs += 1
                        if command != 'pdflatex':
                            break
                    for nrun in range(max_runs - n_runs):
                        returncode = executables['pdflatex']().run(
                            language_context.localized_tex_filename)
                        if returncode != 0:
                            sys.exit(returncode)
                        aux_md5 = file_md5(aux_filename)
                        if _latest_aux_md5 == aux_md5:
                            break
                        else:
                            _latest_aux_md5 = aux_md5

        expected_filename = "%s%s" % (language,
                                      executables[commands[-1]].output_extension)
        expected_filepath = os.path.join(
            project_context.source_dirpath, expected_filename
        )
        if not os.path.exists(expected_filepath):
            break

        dist_filepath = os.path.join(project_context.dist_dirpath, expected_filename)
        os.rename(expected_filepath, dist_filepath)
