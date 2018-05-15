import os
import re
import sys
import webbrowser

import click
import pyperclip
import requests


LOOKUPS = [
    'http://www.google.com/search?tbm=isch&q=%s',
    'http://englishdictionary.naver.com/#/search?query=%s',
    'http://www.thesaurus.com/browse/%s',
    'https://www.vocabulary.com/dictionary/%s',
    'http://endic.naver.com/search.nhn?sLn=kr&query=%s',
]


@click.option('--anki-media', envvar='ANKI_MEDIA')
@click.option('-q', '--quiet', '--no-lookup', is_flag=True)
@click.argument('words', nargs=-1)
def command(anki_media, no_lookup, words):
    filenames = []
    for w in words:
        word = w.lower()
        filename = '%s.mp3' % word
        filenames.append((word, filename))
        filepath = os.path.join(anki_media, filename)
        bytes_ = voice_of(word)

        if not no_lookup:
            lookup(word)

        save(filepath, bytes_)
        play(filepath)

    content = '\n'.join('%s [sound:%s]' % (w, fn) for w, fn in filenames)
    pyperclip.copy(content)
    print(content)


def lookup(word):
    for l in LOOKUPS:
        webbrowser.open_new_tab(l % word)


def voice_of(word):
    url = 'http://endic.naver.com/search.nhn?sLn=en&query={}'.format(word)
    page_source = make_request(url).decode('utf-8')

    mo = re.search(r'playlist="([^"]+)"', page_source)
    if mo:
        voice_url = mo.group(1)
        return make_request(voice_url)
    else:
        errexit("Unable to find voice for '%s'" % word)


def make_request(url):
    response = requests.get(url)
    return response.content


def save(filepath, bytes_):
    with open(filepath, 'wb') as f:
        f.write(bytes_)


def play(filepath):
    cmd = "( afplay '%s' & )" % filepath
    os.system(cmd)


def errexit(message):
    print(message, file=sys.stderr)
    sys.exit(1)
