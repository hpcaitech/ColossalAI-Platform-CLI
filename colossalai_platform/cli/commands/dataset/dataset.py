import click

from colossalai_platform.cli.aliased_group import AliasedGroup, CONTEXT_SETTINGS
from colossalai_platform.cli.commands.dataset.upload_dir import upload_dir


@click.command(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS, help="Manage your datasets")
def dataset():
    """TODO(ofey404): build this after login feature"""
    pass


dataset.add_command(upload_dir)
