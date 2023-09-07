import click

from colossalai_platform.cli.aliased_group import AliasedGroup, CONTEXT_SETTINGS
from colossalai_platform.cli.commands.project.create import create
from colossalai_platform.cli.commands.project.init import init
from colossalai_platform.cli.commands.project.list import list_project


@click.command(cls=AliasedGroup,
               context_settings=CONTEXT_SETTINGS,
               help="Manage your projects for training and inference")
def project():
    pass


# register command
project.add_command(init)
project.add_command(create)
project.add_command(list_project)
