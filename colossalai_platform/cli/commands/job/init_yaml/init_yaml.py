from pathlib import Path
import sys

import click

from colossalai_platform.cli.commands.job.init_yaml.yaml import JobYaml
from colossalai_platform.cli.context import CommandContext

@click.command(name="init-yaml", help="init job yaml")
@click.option('--project-id', '-p', required=True, help='Project ID, run `cap project list` to find it.')
@click.option('--output-path', '-o', default="job.yaml", required=False, help='Output file path. Default is `job.yaml`.')
@click.option('--stdout', is_flag=True, help='Print to stdout, instead of writing to file. Override --output-path.')
@click.pass_context
def init_yaml(
        ctx: click.Context,
        project_id: str,
        output_path: Path,
        stdout: bool,
):
    cmd_ctx = ctx.find_object(CommandContext)
    assert cmd_ctx

    # TODO(ofey404): get the latest version
    version = cmd_ctx.api.project().version_list(project_id)[-1]

    hyperparameters = cmd_ctx.api.project().hyperparameters(project_id, version)
    print(f"hyperparameters: {hyperparameters}")
    images = cmd_ctx.api.job().images()
    print(f"images: {images}")

    if stdout:
        JobYaml().dump_str_with_comment(sys.stdout)
        return
    with open(output_path, 'wt') as f:
        JobYaml().dump_str_with_comment(f)
        print(f"Job yaml is written to {output_path}")
