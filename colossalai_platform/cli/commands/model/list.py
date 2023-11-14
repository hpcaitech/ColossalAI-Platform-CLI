import click
import textwrap

from colossalai_platform.cli.context import CommandContext

@click.command(name="list", help="list models")
@click.pass_context
def list_model(ctx: click.Context,):
    cmd_ctx = ctx.find_object(CommandContext)
    assert cmd_ctx

    models = cmd_ctx.api.model().list()

    for m in models:
        _pretty_print_model(m)


def _pretty_print_model(
        d: "ModelListResponse",
        indent: int = 2,
):
    s = f"""Name: {d.datasetName}
ID: {d.datasetId}
Full Name: {d.datasetFullName}
Description: {d.datasetDescription}
Created At: {d.createAt}
"""
    click.echo(textwrap.indent(s, " " * indent))
