import os
import shutil
import requests

import click

from colossalai_platform.cli.aliased_group import (CONTEXT_SETTINGS, AliasedGroup)
from colossalai_platform.cli.context import BaseCommandContext


@click.command(context_settings=CONTEXT_SETTINGS, help="Login to the platform")
@click.option(
    '--dont-save-credential',
    is_flag=True,
    help='Do not save username and password to local config file',
)
@click.pass_context
def login(ctx: click.Context, dont_save_credential: bool):
    # TODO(ofey404): In first version we build interactive login,
    #                and save token to local dir.

    base_ctx = ctx.find_object(BaseCommandContext)
    assert base_ctx

    print(f"""## Login to the platform.

By default the username and password will be saved to {str(base_ctx.config_path())},
use --dont-save-credential if you don't want this behavior.
""")
    username = click.prompt("Username")
    password = click.prompt("Password (Hide input)", hide_input=True)

    # TODO(ofey404): do the request

    if dont_save_credential:
        return

    base_ctx.config.username = username
    base_ctx.config.password = password
    base_ctx.dump_to_dir()
