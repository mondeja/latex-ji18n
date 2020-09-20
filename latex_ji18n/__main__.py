#!/usr/bin/env python

import os

import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument(
    "project_path",
    envvar="LATEX_JI18N_PROJECT_PATH",
    type=click.Path(exists=True),
    nargs=-1,
)
@click.option(
    "-c", "--commands",
    default='pdflatex',
    required=False,
    type=str
)
def build(project_path, commands):
    """Build with Latex the distribution files of the project located at
    the path passed as PROJECT_PATH argument (current working directory
    by default)."""
    from latex_ji18n.commands.build import run
    if not project_path:
        project_path = os.getcwd()
    elif isinstance(project_path, tuple):
        project_path = project_path[0]
    kwargs = {}
    if commands:
        kwargs['commands'] = commands.split(',')
    run(project_path=os.path.abspath(project_path), **kwargs)


if __name__ == "__main__":
    cli()
