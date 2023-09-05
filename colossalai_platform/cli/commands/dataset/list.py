import click
import textwrap

from colossalai_platform.cli.api import DatasetListResponse
from colossalai_platform.cli.context import CommandContext


@click.command(name="list", help="list datasets")
@click.pass_context
def list_dataset(ctx: click.Context,):
    cmd_ctx = ctx.find_object(CommandContext)
    assert cmd_ctx

    datasets = cmd_ctx.api.dataset().list()

    for i, d in enumerate(datasets):
        _pretty_print_dataset(d)


def _pretty_print_dataset(
    d: DatasetListResponse,
    indent: int = 2,
):
    s = f"""Name: {d.datasetName}
ID: {d.datasetId}
Full Name: {d.datasetFullName}
Description: {d.datasetDescription}
Created At: {d.createdAt}
"""
    click.echo(textwrap.indent(s, " " * indent))
