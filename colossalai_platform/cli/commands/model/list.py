from typing import List

import click
import textwrap

from colossalai_platform.cli.api.model import ModelListResponse
from colossalai_platform.cli.context import CommandContext


@click.command(name="list", help="list models")
@click.option('--tag', multiple=True, type=str, help='The tag(s) to filter the model.')
@click.pass_context
def list_model(
        ctx: click.Context,
        tag: List[str]
):
    cmd_ctx = ctx.find_object(CommandContext)
    assert cmd_ctx

    models = cmd_ctx.api.model().list(
        tags=tag
    )
    for m in models:
        _pretty_print_model(m)


def _pretty_print_model(
        m: ModelListResponse,
        indent: int = 2,
):
    s = f"""Name: {m.modelName}
ID: {m.modelId}
Full Name: {m.modelFullName}
Description: {m.modelDescription}
Created At: {m.createdAt}
"""
    click.echo(textwrap.indent(s, " " * indent))
