import click

from colossalai_platform.cli.aliased_group import (CONTEXT_SETTINGS, AliasedGroup)
from colossalai_platform.cli.context import BaseCommandContext

from .commands import project, dataset, login


@click.command(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx: click.Context):
    ctx.obj = BaseCommandContext()


# add command group
cli.add_command(login)
cli.add_command(project)
cli.add_command(dataset)
