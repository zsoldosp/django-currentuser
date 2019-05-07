.PHONY: clean-python clean-build docs clean-tox
PYPI_SERVER?=pypi
GIT_REMOTE_NAME?=origin
SHELL=/bin/bash
VERSION=$(shell python -c"import django_currentuser as m; print(m.__version__)")

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-python - remove Python file artifacts"
	@echo "clean-tox - remove test artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - git tag the current version which creates a new pypi package with travis-ci's help"

clean: clean-build clean-python clean-tox

clean-build:
	rm -fr build/
	rm -fr dist/
	find -name *.egg-info -type d | xargs rm -rf

clean-python:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -type d -exec rm -rf {} +

clean-tox:
	if [[ -d .tox ]]; then rm -r .tox; fi

lint:
	flake8 django_currentuser tests --max-complexity=10

test:
	python manage.py test testapp --traceback

test-all: clean-tox
	tox

coverage:
	coverage run --source django_currentuser setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs: outfile=/tmp/readme-errors
docs:
	rst2html.py README.rst > /dev/null 2> ${outfile}
	cat ${outfile}
	test 0 -eq `cat ${outfile} | wc -l`

release: TAG:=v${VERSION}
release: exit_code=$(shell git ls-remote ${GIT_REMOTE_NAME} | grep -q tags/${TAG}; echo $$?)
release:
ifeq ($(exit_code),0)
	@echo "Tag ${TAG} already present"
else
	git tag -a ${TAG} -m"${TAG}"; git push --tags ${GIT_REMOTE_NAME}
endif
