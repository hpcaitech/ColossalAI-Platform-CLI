import os
import shutil

import click

from colossalai_platform.cli.aliased_group import (CONTEXT_SETTINGS,
                                                   AliasedGroup)


@click.command(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS, help="Manage your templates for training and inference")
def template():
    pass


@click.command(help='Initialize Your ColossalAI Template')
@click.argument('name', required=1, type=str)
def init(name):
    # get current directory
    current_dir = os.getcwd()

    # create the template directory
    user_template_dir = os.path.join(current_dir, name)

    if os.path.exists(user_template_dir):
        click.echo(f"Error: The template {name} already exists in {current_dir}")
        exit()
    else:
        os.mkdir(user_template_dir)

    # get the current file path
    # the templates files are located in current_file_path/templates
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    template_file_dir = os.path.join(current_file_path, 'templates')

    # copy the files in template_file_dir to template_dir
    for file_name in os.listdir(template_file_dir):
        # skip this file
        if file_name in ['__init__.py', '__pycache__']:
            continue
        
        src_path = os.path.join(template_file_dir, file_name)
        dst_path = os.path.join(user_template_dir, file_name)
        shutil.copy(src_path, dst_path)


# register command
template.add_command(init)