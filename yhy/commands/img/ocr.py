import io

import click
from google.cloud import vision
from PIL import ImageGrab


@click.option('-l', '--lang', default='en')
def command(lang):
    client = vision.ImageAnnotatorClient()

    img = ImageGrab.grabclipboard()
    if img is None:
        raise click.UsageError('Clipboard does not contain image data')
    b = io.BytesIO()
    img.save(b, 'png')

    image = vision.types.Image(content=b.getvalue())
    image_context = vision.types.ImageContext(language_hints=[lang])
    response = client.text_detection(image=image, image_context=image_context)
    text = response.full_text_annotation.text
    text = text.strip()
    click.echo(text)
