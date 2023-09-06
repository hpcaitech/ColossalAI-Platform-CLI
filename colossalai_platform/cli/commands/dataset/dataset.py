import click

from colossalai_platform.cli.aliased_group import AliasedGroup, CONTEXT_SETTINGS
from colossalai_platform.cli.commands.dataset.create import create
from colossalai_platform.cli.commands.dataset.list import list_dataset
from colossalai_platform.cli.commands.dataset.upload_dir import upload_dir


@click.command(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS, help="Manage your datasets")
def dataset():
    pass


dataset.add_command(upload_dir)
dataset.add_command(list_dataset)
dataset.add_command(create)
