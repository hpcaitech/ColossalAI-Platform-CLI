import click

from colossalai_platform.cli.aliased_group import AliasedGroup, CONTEXT_SETTINGS

@click.command(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS, help="Manage your models")
def model():
    pass