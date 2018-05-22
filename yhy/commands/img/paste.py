import click

from yhy import require
from yhy.core.img import clipboard_img, save


@click.argument('path', type=click.Path(exists=False))
def command(path):
    require.directory(path)
    img = clipboard_img()
    save(img, path)
