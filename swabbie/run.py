import click

from swabbie.utils.list import List
from swabbie.utils.clean import Clean
from swabbie.utils.reference import Reference


@click.group()
@click.version_option()
@click.pass_context
def cli(ctx):
    pass

@cli.command()
def nuke():
    click.echo(Clean.nuke())

@cli.command()
def clean():
    click.echo(Clean.clean())

@cli.command()
@click.option('--all/--live', default=True)
def list(all):
    if all:
        click.echo(List.display_list('Images', List.Commands.ALL_IMAGE))
        click.echo(List.display_list('Containers', List.Commands.ALL_CONTAINER))
    else:
        click.echo(List.display_list('Live Images', List.Commands.LIVE_IMAGE))
        click.echo(List.display_list('Live Containers', List.Commands.LIVE_CONTAINER))

@cli.command()
def count():
    click.echo("Images\n\tNon-Dangling {}\n\tAll {}\n\n" \
             "Containers\n\tRunning {}\n\tAll {}".format(
        List.get_count(List.Commands.LIVE_IMAGE),
        List.get_count(List.Commands.ALL_IMAGE),
        List.get_count(List.Commands.LIVE_CONTAINER),
        List.get_count(List.Commands.ALL_CONTAINER)
    ))

@cli.command()
@click.option('--c', type=click.Choice(['all', 'runimg', 'runcntr']), default='all')
@click.option('--n', type=str, default='', help='Name of image or container that you want to run')
def ref(c, n):
    if c == 'all' or c == 'runimg':
        img_cmd = Reference.Shell.RUN_IMAGE.format(n) if n else Reference.Shell.RUN_IMAGE
        click.echo('Run image: {}'.format(img_cmd))

    if c == 'all' or c == 'runcntr':
        container_cmd = Reference.Shell.RUN_CONTAINER.format(n) if n else Reference.Shell.RUN_CONTAINER
        click.echo('Run container: {}'.format(container_cmd))