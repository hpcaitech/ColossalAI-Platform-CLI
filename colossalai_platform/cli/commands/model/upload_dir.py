import logging

import click
import pathlib

from colossalai_platform.cli.api.model import DeleteFilesRequest
from colossalai_platform.cli.commands.util import do_you_want_to_continue, relative_posix_path, get_all_local_file_path
from colossalai_platform.cli.context import CommandContext

LOGGER = logging.getLogger(__name__)

@click.command(help="Upload the whole directory as a model")
@click.argument('model_id', required=1, type=str)
@click.argument('directory', required=1, type=pathlib.Path)
@click.option('--yes', '-y', is_flag=True, help='Skip confirmation.')
@click.pass_context
def upload_dir(
        ctx: click.Context,
        model_id: str,
        directory: pathlib.Path,
        yes: bool,
):
    cmd_ctx = ctx.find_object(CommandContext)
    assert cmd_ctx

    # check if the dataset exists
    try:
        info = cmd_ctx.api.model().info(model_id)
    except Exception as e:
        click.echo(e)
        ctx.exit(1)

    click.echo(f"""Upload overview:
    Local directory: {directory.absolute()}
    Model:
        ID: {model_id}
        Name: {info.modelName}
        FullName: {info.modelFullName}
        Description: {info.modelDescription}
        CreatedAt: {info.createdAt}

The model content would be overwritten.
""")

    if not yes:
        do_you_want_to_continue(ctx)

    click.echo(f"Cleaning model {model_id}...")

    try:
        cmd_ctx.api.model().delete_files(DeleteFilesRequest(
            id=model_id,
            folders=[""],
        ))
    except Exception as e:
        click.echo(e)
        ctx.exit(1)

    click.echo(f"Uploading directory {directory} as model {model_id}...")

    for local_file_path in get_all_local_file_path(directory):
        storage_path = relative_posix_path(directory, local_file_path)

        click.echo(f"{local_file_path} => {storage_path}")

        cmd_ctx.api.model().upload_local_file(
            model_id=model_id,
            storage_path=storage_path,
            local_file_path=local_file_path,
        )

    click.echo("Done.")
    click.echo(f"Directory {directory} uploaded as model {model_id}.")
