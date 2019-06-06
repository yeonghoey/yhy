import os
from pathlib import Path
import re
import shutil

import click

from yhy import require


@click.argument('source_dir', type=click.Path(exists=True))
@click.argument('source_fps', type=int)
@click.argument('target_fps', type=int)
def command(source_dir, source_fps, target_fps):
    if source_fps % target_fps != 0:
        raise click.UsageError('Source FPS should be divisible by target FPS')
    step = source_fps // target_fps 

    source_dir = Path(source_dir)
    target_dir = Path('{}-{}fps'.format(source_dir, target_fps))
    if target_dir.is_dir():
        raise click.UsageError('"{}/" exists!'.format(target_dir))

    require.directory(target_dir)

    files = [p for p in source_dir.iterdir() if p.is_file()]
    plan = []
    for src in sorted(files):
        name = src.name
        m = re.search('\d+', name)
        if m is None:
            continue

        x = m.group()
        n = int(x)

        if n % step == 0:
            k = n // step
            y = '{:0{ndigits}d}'.format(k, ndigits=len(x))
            dst = target_dir / name.replace(x, y)
            plan.append((src, dst))

    lines = ['%s -> %s' % (src, dst) for src, dst in plan]
    click.echo_via_pager('\n'.join(lines))
    if click.confirm('Execute?'):
        for src, dst in plan:
            shutil.copyfile(src, dst)

    else:
        click.echo('Canceled.')
