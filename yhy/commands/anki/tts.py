from hashlib import sha1
import os
import random

import click
from google.cloud import texttospeech
from prompt_toolkit import PromptSession

import pyperclip


@click.option('--anki-media', envvar='ANKI_MEDIA')
def command(anki_media):
    session = PromptSession()
    speak = make_speak()
    last = ''
    while True:
        text = session.prompt('TTS > ')
        text = text.strip()
        if not text:
            if last:
                text, path = last
                copy_and_play(text, path)
            continue
        sound, ext = speak(text)
        path = path_for(anki_media, sound, ext)
        write(path, sound)
        copy_and_play(text, path)
        last = (text, path)


def make_speak():
    client = texttospeech.TextToSpeechClient()
    conf = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    def speak(text):
        si = texttospeech.types.SynthesisInput(text=text)
        vo = pick_voice()
        response = client.synthesize_speech(si, vo, conf)
        return (response.audio_content, '.mp3')

    return speak


def pick_voice():
    V = texttospeech.types.VoiceSelectionParams
    voices = [
        V(language_code='en-US', name='en-US-Wavenet-A'),
        V(language_code='en-US', name='en-US-Wavenet-B'),
        V(language_code='en-US', name='en-US-Wavenet-C'),
        V(language_code='en-US', name='en-US-Wavenet-D'),
        V(language_code='en-US', name='en-US-Wavenet-E'),
        V(language_code='en-US', name='en-US-Wavenet-F'),
    ]
    return random.choice(voices)


def path_for(anki_media, sound, ext):
    name = name_for(sound)
    return os.path.join(anki_media, name + ext)


def name_for(sound):
    ho = sha1()
    ho.update(sound)
    return ho.hexdigest()


def write(path, sound):
    with open(path, 'wb') as f:
        f.write(sound)


def copy_and_play(text, path):
    sl = soundlink(path)
    print(sl)
    copy(f'{text}\n{sl}')
    last = path
    play(path)


def soundlink(path):
    name = os.path.basename(path)
    return f'[sound:{name}]'


def copy(s):
    pyperclip.copy(s)


def play(path):
    cmd = f"( afplay '{path}' & )"
    os.system(cmd)
