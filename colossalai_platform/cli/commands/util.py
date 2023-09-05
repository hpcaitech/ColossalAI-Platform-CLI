import click


def do_you_want_to_continue(ctx: click.Context):
    y = click.prompt("Do you want to continue [y/N]")
    if y.lower() != "y":
        click.echo("Aborted!")
        ctx.exit(1)
