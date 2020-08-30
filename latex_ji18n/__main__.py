#!/usr/bin/env python

import os

import click


@click.group()
def cli():
    pass


@click.argument(
    "project_path",
    envvar="LATEX_JI18N_PROJECT_PATH",
    type=click.Path(exists=True),
    nargs=-1,
)
@cli.command()
def build(project_path):
    from latex_ji18n.commands.build import run
    if not project_path:
        project_path = os.getcwd()
    run(project_path=os.path.abspath(project_path))


if __name__ == "__main__":
    cli()
