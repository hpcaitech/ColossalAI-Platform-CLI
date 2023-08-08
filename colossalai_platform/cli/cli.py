import logging

import click

from colossalai_platform.cli.aliased_group import (CONTEXT_SETTINGS, AliasedGroup)
from colossalai_platform.cli.context import BaseCommandContext
from .api.api import LoginError

from .commands import project, dataset, configure

LOGGER = logging.getLogger(__name__)


def configure_logging(debug=False):
    if debug:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(
        format=f"%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=level,
    )


REQUIRE_LOGIN = ["dataset"]


@click.command(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
@click.option("--debug", is_flag=True, help="Enable debug logging.")
@click.pass_context
def cli(
    ctx: click.Context,
    debug: bool,
):
    configure_logging(debug)
    ctx.obj = BaseCommandContext()

    if ctx.invoked_subcommand in REQUIRE_LOGIN:
        # TODO(ofey404): persist token to file, rather than login every time
        try:
            ctx.obj.api.login()
        except LoginError as e:
            click.echo(e)
            ctx.exit(1)


# add command group
cli.add_command(configure)
cli.add_command(project)
cli.add_command(dataset)
