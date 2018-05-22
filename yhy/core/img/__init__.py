import click
from PIL import ImageGrab


def clipboard_img():
    img = ImageGrab.grabclipboard()
    if img is None:
        raise click.UsageError('Clipboard does not contain image data')
    else:
        return img


def save(img, path):
    img.save(path)
