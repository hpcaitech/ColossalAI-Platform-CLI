import pathlib

import click

from colossalai_platform.cli.api import ProjectNotFoundError, DeleteFilesRequest, NoObjectToDeleteError
from colossalai_platform.cli.commands.util import do_you_want_to_continue, get_all_local_file_path, relative_posix_path
from colossalai_platform.cli.context import CommandContext


@click.command(help="Upload the whole directory as a project")
@click.argument('project_id', required=1, type=str)
@click.argument('directory', required=1, type=pathlib.Path)
@click.option('--yes', '-y', is_flag=True, help='Skip confirmation.')
@click.pass_context
def upload_dir(
    ctx: click.Context,
    project_id: str,
    directory: pathlib.Path,
    yes: bool,
):
    cmd_ctx = ctx.find_object(CommandContext)
    assert cmd_ctx

    try:
        info = cmd_ctx.api.project().info(project_id)
    except ProjectNotFoundError as e:
        click.echo(e)
        ctx.exit(1)

    click.echo(f"""Upload overview:
    Local directory: {directory.absolute()}
    Dataset:
        ID: {project_id}
        Name: {info.projectName}
        Description: {info.projectDescription}
        CreatedAt: {info.createAt}

The project content would be overwritten.
""")

    if not yes:
        do_you_want_to_continue(ctx)

    click.echo(f"Cleaning project {project_id}...")

    try:
        cmd_ctx.api.project().delete_files(DeleteFilesRequest(
            id=project_id,
            folders=[""],
        ))
    except NoObjectToDeleteError:
        pass

    click.echo(f"Uploading directory {directory} as project {project_id}...")

    for local_file_path in get_all_local_file_path(directory):
        storage_path = relative_posix_path(directory, local_file_path)

        click.echo(f"{local_file_path} => {storage_path}")

        cmd_ctx.api.project().upload_local_file(
            project_id=project_id,
            storage_path=storage_path,
            local_file_path=local_file_path,
        )

    click.echo("Done.")
    click.echo(f"Directory {directory} uploaded as project {project_id}.")
