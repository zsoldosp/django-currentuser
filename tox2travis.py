#!/usr/bin/env python
import os
import subprocess


class ToxToTravis:

    def __init__(self, cwd):
        self.cwd = cwd

    def parse_tox(self):
        proc = subprocess.Popen(
            "tox -l", shell=True, stdout=subprocess.PIPE, cwd=self.cwd)
        self.tox_lines = proc.stdout.read().strip().split('\n')
        self.parse_python_versions()

    def parse_python_versions(self):
        tox_pys = set([])
        djangos = set([])
        tox_py_to_djangos = {}
        for tox_line in self.tox_lines:
            py, env = tox_line.split('-')
            tox_pys.add(py)
            djangos.add(env)
            tox_py_to_djangos.setdefault(py, [])
            tox_py_to_djangos[py].append(env)

        self.djangos = sorted(djangos)
        self.tox_pys = sorted(tox_pys)
        self.tox_py_to_djangos = tox_py_to_djangos

    def write_travis(self):
        lines = self.setup_python() + self.matrix() + self.test_command()
        print('\n'.join(lines))

    def setup_python(self):
        return [
            'dist: xenial',
            'language: python',
            'before_install:',
            '  - sudo apt-get -qq update',
            '  - sudo apt-get install -y make sed',
            'install:',
            '  - pip install tox',
        ]

    def matrix(self):
        self.tox2travis_py = dict(
            py27='2.7',
            py34='3.4',
            py35='3.5',
            py36='3.6',
        )
        output = [
            'matrix:',
            '  include:',
        ]
        for tox_py, djangos in self.tox_py_to_djangos.items():
            tox_envs_gen = ('-'.join((tox_py, d)) for d in djangos)
            item = [
                '    - python: "%s"' % self.tox2travis_py[tox_py],
                '      env: TOX_ENVS=%s' % ','.join(tox_envs_gen),
            ]
            output += item
        return output

    def test_command(self):
        return [
            'script:',
            '  - tox -e $TOX_ENVS',
            'before_deploy: "make pre-deploy"',
            'deploy:',
            '  provider: pypi',
            '  user: "paessler_bis"',
            '  password:',
            '    secure: "N+ark/iPL3Y8/ew9i3y0IQITVFRN6AQmUirG6YBIaNt5jw+N081qYuPtco7AwcbOWBiYz9JX6k6xfFcWGw0+bDUkpGZQkVgBdqAaQUj6kEzpyNU5vsyHY7jqBAYdkjReTXf7s+ZtNCIs/qLuhgipYIOEwCtv5cUkC5WMFa1/wIWKq7LwkS6TmrjbFxC0+fXna9xwa6hdUSkz3t0B8d81tEln5TbJovlViJObM1GqxQPrU8UUoGvdOWzaTdLLWB70Z1M70Gy+XwPba+Ce6tJsRzoKpELCEYuNyTPivPAbNmzqpUB+LzBNg90X7WPO2cfI1mlHBOOV1l8ogac/wEJvxQyNMg08z07JQUJfg6sbBsQMSc7EWj46owCnvvPZ6xQ+wkz3h+HEwYTxTFuoO/9/2LIpXvMqmO6n7WJ/jpBlJA/2ejWX1Eb8EXWBsNm6/8EVZLz5JSnFhyxZ6XxB83rsGGSGtQy4CR2JZisies8RqWNATF+6UGXd4ydPi9WXr4/BsPRMnObWAZrFUzzqgoLpkKQ/YTSqn55Id0PfL9veCWVwrWel5fvBB8Pkad3eG+VVhszgTzlcQyni8hZbI1StCpLIjGqWRxhp7F7fPBs+MBUKTX7P/wrCwAhn67i54rzvdc0Tk1BQuBVa7b6T+o1dO9xtMnz811Pj817bhF9oVvM="',
            '  distributions: sdist bdist_wheel',
            '  on:',
            '    tags: true',
            '    branch:',
            '      - master',
            '      - /v?(\d+\.)?(\d+\.)?(\*|\d+)$/',
        ]


def main():
    cwd = os.path.abspath(os.path.dirname(__file__))
    ttt = ToxToTravis(cwd)
    ttt.parse_tox()
    ttt.write_travis()


if __name__ == '__main__':
    main()
