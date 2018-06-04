from hashlib import sha1

import click
from PIL import ImageGrab


def clipboard_img(half=False):
    img = ImageGrab.grabclipboard()

    if img is None:
        raise click.UsageError('Clipboard does not contain image data')

    if half:
        img = scaled(img, 0.5)

    return img


def hexhash(img):
    ho = sha1()
    ho.update(img.tobytes())
    return ho.hexdigest()

def save(img, path):
    img.save(path)


def scaled(img, s):
    w, h = img.size
    return img.resize((int(w*s), int(h*s)))
