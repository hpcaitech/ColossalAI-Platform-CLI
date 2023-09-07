import pathlib
from typing import Iterable

import click


def do_you_want_to_continue(ctx: click.Context):
    y = click.prompt("Do you want to continue [y/N]")
    if y.lower() != "y":
        click.echo("Aborted!")
        ctx.exit(1)


def get_all_local_file_path(directory) -> Iterable[pathlib.Path]:
    directory = pathlib.Path(directory)
    return (p for p in directory.glob("**/*") if p.is_file())


def relative_posix_path(
    directory: pathlib.Path,
    local_file_path: pathlib.Path,
):
    assert directory in local_file_path.parents
    return local_file_path.relative_to(directory).as_posix()
