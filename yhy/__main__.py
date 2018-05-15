import click

from yhy import commands


@click.group()
def cli():
    pass


commands.build(cli,
               commands.__path__,
               commands.__package__)


if __name__ == '__main__':
    cli()
