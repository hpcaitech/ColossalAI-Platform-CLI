import os
import shutil

import click

from colossalai_platform.cli.aliased_group import (CONTEXT_SETTINGS, AliasedGroup)


@click.command(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS, help="Manage your datasets")
def dataset():
    """TODO(ofey404): build this after login feature"""
    pass
