import click

from colossalai_platform.cli.aliased_group import AliasedGroup, CONTEXT_SETTINGS
from colossalai_platform.cli.commands.model.create import create
from colossalai_platform.cli.commands.model.list import list_model
from colossalai_platform.cli.commands.model.upload_dir import upload_dir


@click.command(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS, help="Manage your models")
def model():
    pass

model.add_command(list_model)
model.add_command(create)
model.add_command(upload_dir)
