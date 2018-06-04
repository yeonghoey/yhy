from pathlib import Path


def directory(path):
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
