.PHONY: clean-pyc clean-build docs clean-tox
PYPI_SERVER?=pypi
GIT_REMOTE_NAME?=origin
SHELL=/bin/bash
VERSION=$(shell python -c"import django_currentuser as m; print(m.__version__)")

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "tag - tag the current version and push it to ${GIT_REMOTE_NAME}"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean: clean-build clean-pyc clean-tox

clean-build:
	rm -fr build/
	rm -fr dist/
	find -name *.egg-info -type d | xargs rm -rf

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -type d -exec rm -rf {} +

lint:
	flake8 django_currentuser tests --max-complexity=10

test:
	python manage.py test testapp --traceback

clean-tox:
	if [[ -d .tox ]]; then rm -r .tox; fi

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

tag: TAG:=v${VERSION}
tag: exit_code=$(shell git ls-remote ${GIT_REMOTE_NAME} | grep -q tags/${TAG}; echo $$?)
tag:
ifeq ($(exit_code),0)
	@echo "Tag ${TAG} already present"
else
	git tag -a ${TAG} -m"${TAG}"; git push --tags ${GIT_REMOTE_NAME}
endif

package: clean
	python setup.py sdist
	python setup.py bdist_wheel

release: whl=dist/django_currentuser-${VERSION}-py2.py3-none-any.whl
release: clean package docs tag
	# https://packaging.python.org/distributing/
	test -f ${whl}
	echo "if the release fails, setup a ~/pypirc file as per https://docs.python.org/2/distutils/packageindex.html#pypirc"
	twine upload dist/* -r ${PYPI_SERVER}
