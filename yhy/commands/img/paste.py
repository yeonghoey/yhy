import os

import click

from yhy import require
from yhy.core.img import clipboard_img, save


@click.option('-C', '--directory', type=click.Path(exists=False))
def command(directory):
    img, hash_ = clipboard_img()
    filename = f'{hash_}.png'

    if not directory:
        path = filename
    else:
        require.directory(directory)
        path = os.path.join(directory, filename)

    save(img, path)
    click.echo(path)
