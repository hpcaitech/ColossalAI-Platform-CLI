import textwrap

import click

from colossalai_platform.cli.api.job import JobListResponse
from colossalai_platform.cli.context import CommandContext


@click.command(name="list", help="list jobs")
@click.pass_context
def list_job(ctx: click.Context):
    cmd_ctx = ctx.find_object(CommandContext)
    assert cmd_ctx

    jobs = cmd_ctx.api.job().list()

    for j in jobs:
        _pretty_print_job(j)


def _pretty_print_job(
        d: JobListResponse,
        indent: int = 2,
):
    s = f"""Name: {d.jobName}
ID: {d.jobId}
Status: {d.jobStatus}
Description: {d.jobDescription}
Created At: {d.createdAt}
"""
    click.echo(textwrap.indent(s, " " * indent))
