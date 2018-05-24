SHELL = /bin/sh

init:
	pipenv install --dev

deploy:
	-rm -rf build dist .egg yhy.egg-info
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*
