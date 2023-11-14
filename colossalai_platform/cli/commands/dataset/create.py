import click

from colossalai_platform.cli.api import ApiError
from colossalai_platform.cli.commands.util import do_you_want_to_continue
from colossalai_platform.cli.context import CommandContext


@click.command(help="Create an empty dataset")
@click.option('--yes', '-y', is_flag=True, help='Skip confirmation.')
@click.pass_context
def create(
    ctx: click.Context,
    yes: bool,
):
    cmd_ctx = ctx.find_object(CommandContext)
    assert cmd_ctx

    click.echo(f"Create an empty dataset, user: {cmd_ctx.config.username}")
    name = click.prompt("  Dataset name")
    description = click.prompt("  Dataset description")

    if not yes:
        do_you_want_to_continue(ctx)

    try:
        dataset_id = cmd_ctx.api.dataset().create(name, description)
    except ApiError as e:
        click.echo(e)
        ctx.exit(1)

    click.echo(f"Dataset created successfully, id: {dataset_id}")
