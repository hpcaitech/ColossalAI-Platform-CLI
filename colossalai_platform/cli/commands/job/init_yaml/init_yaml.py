import click
from colossalai_platform.cli.context import CommandContext

@click.command(name="init-yaml", help="init job yaml")
@click.option('--project-id', '-p', required=True, help='Project ID, run `cap project list` to find it.')
@click.pass_context
def init_yaml(
        ctx: click.Context,
        project_id: str,
):
    cmd_ctx = ctx.find_object(CommandContext)
    assert cmd_ctx

    # TODO(ofey404): get the latest version
    version = cmd_ctx.api.project().version_list(project_id)[-1]

    hyperparameters = cmd_ctx.api.project().hyperparameters(project_id, version)
    print(f"hyperparameters: {hyperparameters}")
    images = cmd_ctx.api.job().images()
    print(f"images: {images}")
