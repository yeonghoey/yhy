from hashlib import sha1

import click
from PIL import ImageGrab


def clipboard_img():
    img = ImageGrab.grabclipboard()
    if img is None:
        raise click.UsageError('Clipboard does not contain image data')
    else:
        h = sha1()
        h.update(img.tobytes())
        return (img, h.hexdigest())


def save(img, path):
    img.save(path)
