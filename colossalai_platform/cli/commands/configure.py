import click

from colossalai_platform.cli.aliased_group import (CONTEXT_SETTINGS, AliasedGroup)
from colossalai_platform.cli.api import ApiError
from colossalai_platform.cli.context import CommandContext

LOGIN_URL = "https://luchentech.com/api/user/login"


@click.command(context_settings=CONTEXT_SETTINGS, help="Login to the platform")
@click.pass_context
def configure(ctx: click.Context):
    # TODO(ofey404): In first version we build interactive login,
    #                and save username/password to local dir.

    cmd_ctx = ctx.find_object(CommandContext)
    assert cmd_ctx

    cmd_ctx.config.username = click.prompt("Username")
    cmd_ctx.config.password = click.prompt("Password (Hide input)", hide_input=True)

    try:
        cmd_ctx.api.user().login()
    except ApiError as e:
        click.echo(e)
        ctx.exit(1)

    cmd_ctx.dump_to_dir()
