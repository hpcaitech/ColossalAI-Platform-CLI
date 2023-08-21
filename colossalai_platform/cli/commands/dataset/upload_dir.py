import logging

import click
import pathlib
from typing import Iterable

from colossalai_platform.cli.api import StorageType
from colossalai_platform.cli.context import CommandContext

LOGGER = logging.getLogger(__name__)


@click.command(help="Upload the whole directory as a dataset")
@click.argument('dataset_id', required=1, type=str)
@click.argument('directory', required=1, type=pathlib.Path)
@click.pass_context
def upload_dir(
    ctx: click.Context,
    dataset_id: str,
    directory: pathlib.Path,
):
    cmd_ctx = ctx.find_object(CommandContext)
    assert cmd_ctx

    click.echo(f"Uploading directory {directory} as dataset {dataset_id}...")
    for local_file_path in _get_all_local_file_path(directory):
        storage_path = _relative_posix_path(directory, local_file_path)
        click.echo(f"{local_file_path} => {storage_path}")

        LOGGER.debug(
            f"local_file_path: {local_file_path}, storage_path: {storage_path}, local_file_path: {local_file_path}")
        cmd_ctx.api.upload(
            storage_type=StorageType.DATASET,
            storage_id=dataset_id,
            storage_path=storage_path,
            local_file_path=local_file_path,
        )
    click.echo("Done")


def _get_all_local_file_path(directory) -> Iterable[pathlib.Path]:
    directory = pathlib.Path(directory)
    return (p for p in directory.glob("**/*") if p.is_file())


def _relative_posix_path(
    directory: pathlib.Path,
    local_file_path: pathlib.Path,
):
    assert directory in local_file_path.parents
    return local_file_path.relative_to(directory).as_posix()
