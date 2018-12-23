from hashlib import sha1
import subprocess
import sys
from tempfile import NamedTemporaryFile

import click
from PIL import ImageGrab
from PIL.Image import BICUBIC


def clipboard_img(half=False):
    img = ImageGrab.grabclipboard()

    if img is None:
        raise click.UsageError('Clipboard does not contain image data')

    # NOTE: Calcuate hash before modification like scaling down.
    # This is because the pasting image should be unique as a capture process,
    # not as a resulting image.
    ho = sha1()
    ho.update(img.tobytes())
    hexhash = ho.hexdigest()

    if half:
        img = scaled(img, 0.5)

    return (img, hexhash)


def save(img, path):
    img.save(path)


def copy(img):
    if sys.platform == 'darwin':
        with NamedTemporaryFile(suffix='.png') as f:
            img.save(f.name)
            subprocess.run([
                'osascript', '-e',
                f'set the clipboard to (read "{f.name}" as TIFF picture)'])
    else:
        raise click.UsageError('Supports macOS only')



def scaled(img, s):
    w, h = img.size
    return img.resize((int(w*s), int(h*s)), resample=BICUBIC)
