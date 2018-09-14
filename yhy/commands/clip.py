import sys

import click
import pyperclip


def command():
    text = sys.stdin.read().strip()
    pyperclip.copy(text)
    click.echo(text)
