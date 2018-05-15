import click

from yhy.commands import build


@click.group()
def cli():
    pass


build(cli)


if __name__ == '__main__':
    cli()
