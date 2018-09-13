import sys

import click
import pyperclip


def command():
    text = ''.join(l for l in sys.stdin)
    text = text.strip()
    pyperclip.copy(text)
    click.echo(text)
