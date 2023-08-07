import click

from colossalai_platform.cli.aliased_group import (CONTEXT_SETTINGS, AliasedGroup)
from colossalai_platform.cli.api.api import LoginError
from colossalai_platform.cli.context import BaseCommandContext

LOGIN_URL = "https://luchentech.com/api/user/login"


@click.command(context_settings=CONTEXT_SETTINGS, help="Login to the platform")
@click.pass_context
def configure(ctx: click.Context):
    # TODO(ofey404): In first version we build interactive login,
    #                and save username/password to local dir.

    base_ctx = ctx.find_object(BaseCommandContext)
    assert base_ctx

    base_ctx.config.username = click.prompt("Username")
    base_ctx.config.password = click.prompt("Password (Hide input)", hide_input=True)

    try:
        ctx.obj.api.login()
    except LoginError as e:
        click.echo(e)
        ctx.exit(1)

    base_ctx.dump_to_dir()
