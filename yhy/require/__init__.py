from pathlib import Path


def directory(path, isdir=False):
    p = (Path(path) if isdir else
         Path(path).parent)
    p.mkdir(parents=True, exist_ok=True)
