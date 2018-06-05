import os

import click

from yhy import require
from yhy.core.img import clipboard_img, save


@click.option('-C', '--directory', type=click.Path(exists=False))
@click.option('--half', is_flag=True)
def command(directory, half):
    img, hexhash = clipboard_img(half=half)
    filename = f'{hexhash}.png'

    if not directory:
        path = filename
    else:
        require.directory(directory)
        path = os.path.join(directory, filename)

    save(img, path)
    click.echo(path)
