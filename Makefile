.PHONY: clean-python clean-build docs clean-tox
#PYPI_SERVER?=pypi
PYPI_SERVER?=testpypi
ifeq ($(PYPI_SERVER),testpypi)
	TWINE_PASSWORD=${TEST_TWINE_PASSWORD}
else
	TWINE_PASSWORD=${CURRENTUSER_TWINE_PASSWORD}
endif
RELEASE_PYTHON=python3.8
GIT_REMOTE_NAME?=origin
SHELL=/bin/bash
VERSION=$(shell python3 -c"import django_currentuser as m; print(m.__version__)")
PACKAGE_FILE_TGZ=dist/django_currentuser-${VERSION}.tar.gz
PACKAGE_FILE_WHL=dist/django_currentuser-${VERSION}-py3-none-any.whl

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-python - remove Python file artifacts"
	@echo "clean-tox - remove test artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "tag - git tag the current version which creates a new pypi package with travis-ci's help"
	@echo "package- build the sdist/wheel"
	@echo "release- package, tag, and publush"

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

tag: TAG:=v${VERSION}
tag: exit_code=$(shell git ls-remote ${GIT_REMOTE_NAME} | grep -q tags/${TAG}; echo $$?)
tag:
ifeq ($(exit_code),0)
	@echo "Tag ${TAG} already present"
else
	@echo "git tag -a ${TAG} -m"${TAG}"; git push --tags ${GIT_REMOTE_NAME}"
endif

build-deps: 
	${RELEASE_PYTHON} -m pip install --upgrade build
	${RELEASE_PYTHON} -m pip install --upgrade twine


${PACKAGE_FILE_TGZ}: django_currentuser/ pyproject.toml Makefile setup.py setup.cfg
${PACKAGE_FILE_WHL}: django_currentuser/ pyproject.toml Makefile setup.py setup.cfg
	${RELEASE_PYTHON} -m build

package: build-deps clean-build clean-python ${PACKAGE_FILE} ${PACKAGE_FILE_WHL}


release:  package
ifeq ($(TWINE_PASSWORD),)
	echo TWINE_PASSWORD empty
	echo "USE env vars TEST_TWINE_PASSWORD/CURRENTUSER_TWINE_PASSWORD env vars before invoking make"
	false
endif
	twine check dist/*
	echo "if the release fails, setup a ~/pypirc file as per https://packaging.python.org/en/latest/tutorials/packaging-projects/"
	# env | grep TWINE
	TWINE_PASSWORD=${TWINE_PASSWORD} python3 -m twine upload --repository ${PYPI_SERVER} dist/* --verbose
