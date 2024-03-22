import click

from colossalai_platform.cli.aliased_group import AliasedGroup, CONTEXT_SETTINGS
from colossalai_platform.cli.commands.job.list import list_job


@click.command(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS, help="Manage your jobs")
def job():
    pass


job.add_command(list_job)
