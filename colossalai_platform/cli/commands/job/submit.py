from pathlib import Path

import click
import yaml

from colossalai_platform.cli.api import ApiError
from colossalai_platform.cli.commands.job.internal.jobyaml import JobYaml
from colossalai_platform.cli.context import CommandContext


@click.command(name="submit", help="submit job yaml")
@click.argument('job_yaml', required=1, type=str)
@click.pass_context
def submit(
        ctx: click.Context,
        job_yaml: Path,
):
    cmd_ctx = ctx.find_object(CommandContext)
    assert cmd_ctx

    with open(job_yaml, 'r') as f:
        job_yaml_dict = yaml.safe_load(f)

    j = JobYaml().model_validate(job_yaml_dict)

    try:
        resp = cmd_ctx.api.job().create(j.to_api_req())
        click.echo(f"Job ID {resp.jobId} has been submitted.")
        click.echo(f"Visit {cmd_ctx.config.api_server}/console/job/detail/{resp.jobId}/info for more details.")

    except ApiError as e:
        click.echo(e)
        ctx.exit(1)
