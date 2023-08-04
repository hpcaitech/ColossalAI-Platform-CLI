import click

from colossalai_platform.cli.aliased_group import (CONTEXT_SETTINGS, AliasedGroup)

from .commands import project, dataset, login
from .config import Config

__all__ = ['cli']


@click.command(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx: click.Context,):
    ctx.obj = Config()


# add command group
cli.add_command(login)
cli.add_command(project)
cli.add_command(dataset)
