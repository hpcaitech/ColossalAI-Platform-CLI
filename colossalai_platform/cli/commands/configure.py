import click

from colossalai_platform.cli.aliased_group import (CONTEXT_SETTINGS, AliasedGroup)
from colossalai_platform.cli.api import ApiError
from colossalai_platform.cli.context import CommandContext

LOGIN_URL = "https://luchentech.com/api/user/login"


@click.command(context_settings=CONTEXT_SETTINGS, help="Login to the platform")
@click.pass_context
def configure(ctx: click.Context):
    # TODO(ofey404): In first version we build interactive login,
    #                and save username/password to local dir.

    cmd_ctx = ctx.find_object(CommandContext)
    assert cmd_ctx

    cmd_ctx.config.username = click.prompt("Username")
    cmd_ctx.config.password = click.prompt("Password (Hide input)", hide_input=True)

    try:
        cmd_ctx.api.user().login()
    except ApiError as e:
        click.echo(e)
        ctx.exit(1)

    cmd_ctx.dump_to_dir()

    click.echo("""Login successfully!

Thank you for choosing the ColossalAI Platform!
During our public beta phase, we're actively developing and improving the platform. We appreciate your patience with any user experience issues.

For assistance, visit [doc link](https://docs.platform.luchentech.com/) or reach out anytime.
Your feedback is valuable as we strive to enhance your experience.
""")


# TODO(ofey404): Add a link to the doc page containing `support contact`.
