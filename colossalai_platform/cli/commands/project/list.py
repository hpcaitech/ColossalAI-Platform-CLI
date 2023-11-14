import textwrap

import click

from colossalai_platform.cli.api import ProjectListResponse
from colossalai_platform.cli.context import CommandContext


@click.command(name="list", help="list datasets")
@click.pass_context
def list_project(ctx: click.Context,):
    cmd_ctx = ctx.find_object(CommandContext)
    assert cmd_ctx

    projects = cmd_ctx.api.project().list()

    for i, p in enumerate(projects):
        _pretty_print_project(p)


def _pretty_print_project(
    p: ProjectListResponse,
    indent: int = 2,
):
    s = f"""Name: {p.projectName}
ID: {p.projectId}
Description: {p.projectDescription}
Created At: {p.createAt}
"""
    click.echo(textwrap.indent(s, " " * indent))
