import logging

import click
import pathlib

from colossalai_platform.cli.api import DatasetNotFoundError, DeleteFilesRequest, \
    NoObjectToDeleteError
from colossalai_platform.cli.commands.util import do_you_want_to_continue, get_all_local_file_path, relative_posix_path
from colossalai_platform.cli.context import CommandContext

LOGGER = logging.getLogger(__name__)


@click.command(help="Upload the whole directory as a dataset")
@click.argument('dataset_id', required=1, type=str)
@click.argument('directory', required=1, type=pathlib.Path)
@click.option('--yes', '-y', is_flag=True, help='Skip confirmation.')
@click.pass_context
def upload_dir(
    ctx: click.Context,
    dataset_id: str,
    directory: pathlib.Path,
    yes: bool,
):
    cmd_ctx = ctx.find_object(CommandContext)
    assert cmd_ctx

    # check if the dataset exists
    try:
        info = cmd_ctx.api.dataset().info(dataset_id)
    except DatasetNotFoundError as e:
        click.echo(e)
        ctx.exit(1)

    click.echo(f"""Upload overview:
    Local directory: {directory.absolute()}
    Dataset:
        ID: {dataset_id}
        Name: {info.datasetName}
        FullName: {info.datasetFullName}
        Description: {info.datasetDescription}
        CreatedAt: {info.createAt}

The dataset content would be overwritten.
""")

    if not yes:
        do_you_want_to_continue(ctx)

    click.echo(f"Clearing dataset {dataset_id}...")

    try:
        cmd_ctx.api.dataset().delete_files(DeleteFilesRequest(
            Id=dataset_id,
            folders=[""],
        ))
    except NoObjectToDeleteError:
        pass

    click.echo(f"Uploading directory {directory} as dataset {dataset_id}...")

    for local_file_path in get_all_local_file_path(directory):
        storage_path = relative_posix_path(directory, local_file_path)

        click.echo(f"{local_file_path} => {storage_path}")

        cmd_ctx.api.dataset().upload_local_file(
            dataset_id=dataset_id,
            storage_path=storage_path,
            local_file_path=local_file_path,
        )

    click.echo("Done.")
    click.echo(f"Directory {directory} uploaded as dataset {dataset_id}.")
