from pathlib import Path
from string import Template

import click
from lxml import html
import requests


URL = 'https://www.acmicpc.net/problem/%s'

TEST_NAME = 'main_test.go'
TEST_TEMPLATE = Template('''
package main

import (
	"testing"

	"github.com/yeonghoey/boj/runner"
)

func TestMain(t *testing.T) {
	r := runner.New(t, "go", "run", ".")
	cases := []struct {
		intput, output string
	}{
${samples}
	}
	for _, c := range cases {
		r.Run(c.intput).Want(c.output)
	}
}
'''.strip())


def command():
    problem_dir = Path.cwd()
    problem_id = problem_dir.name

    url = URL % problem_id
    response = requests.get(url)
    if not response.ok:
        raise click.BadParameter('Cannot find the problem: "%s"' % problem_id)

    problem_dir.mkdir(parents=True, exist_ok=True)
    samples = []
    root = html.document_fromstring(response.text)
    for e in root.find_class('sampledata'):
        base = '%s.txt' % e.get('id')
        samples.append(base)
        path = problem_dir / base
        with open(path, 'w') as f:
            f.write(e.text)
        click.echo(base)

    lines = []
    for input, output in zip(samples[0::2], samples[1::2]):
        lines.append('\t\t{"%s", "%s"},' % (input, output))
    samples = '\n'.join(lines)
    content = TEST_TEMPLATE.substitute(samples=samples)
    test_path = problem_dir / TEST_NAME
    with open(test_path, 'w') as f:
        f.write(content)
    click.echo(TEST_NAME)
