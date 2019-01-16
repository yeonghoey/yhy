from pathlib import Path
from string import Template

import click
from lxml import html
import requests


URL = 'https://www.acmicpc.net/problem/%s'


@click.argument('problem-id')
def command(problem_id):
    url = URL % problem_id
    response = requests.get(url)
    if not response.ok:
        raise click.BadParameter('Cannot find the problem')

    problem_dir = Path('./%s' % problem_id)
    problem_dir.mkdir(parents=True, exist_ok=True)
    samples = []
    root = html.document_fromstring(response.text)
    for e in root.find_class('sampledata'):
        base = '%s.txt' % e.get('id')
        samples.append(base)
        path = problem_dir / base
        with open(path, 'w') as f:
            f.write(e.text)
        click.echo(path)

    lines = []
    for input, output in zip(samples[0::2], samples[1::2]):
        lines.append('\t\t{"%s", "%s"},' % (input, output))
    samples = '\n'.join(lines)
    content = MAIN_TEST_GO.substitute(samples=samples)
    test_path = problem_dir / 'main_test.go'
    with open(test_path, 'w') as f:
        f.write(content)
    click.echo(test_path)


MAIN_TEST_GO = Template('''
package main

import (
	"testing"

	"github.com/yeonghoey/boj/runner"
)

func TestSamples(t *testing.T) {
	r := runner.New(t, "go", "run", ".")
	samples := []struct {
		intput, output string
	}{
${samples}
	}
	for _, s := range samples {
		r.Run(s.intput).Want(s.output)
	}
}
'''.strip())
