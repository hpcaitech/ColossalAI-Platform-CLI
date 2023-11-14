import click

from colossalai_platform.cli.aliased_group import AliasedGroup, CONTEXT_SETTINGS
from colossalai_platform.cli.commands.model.list import list_model


@click.command(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS, help="Manage your models")
def model():
    pass

model.add_command(list_model)
