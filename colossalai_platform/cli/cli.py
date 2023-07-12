import click

from colossalai_platform.cli.aliased_group import (CONTEXT_SETTINGS,
                                                   AliasedGroup)

from .commands import template

__all__ = ['cli']


@click.command(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
def cli():
    pass


# add command group
cli.add_command(template)
