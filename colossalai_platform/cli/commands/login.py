import os
import shutil
import requests

import click

from colossalai_platform.cli.aliased_group import (CONTEXT_SETTINGS, AliasedGroup)


@click.command(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS, help="Login to the platform")
@click.argument('username', required=1, type=str)
def login(username):
    pass
