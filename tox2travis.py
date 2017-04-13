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
            py32='3.2',
            py33='3.3',
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
        ]


def main():
    cwd = os.path.abspath(os.path.dirname(__file__))
    ttt = ToxToTravis(cwd)
    ttt.parse_tox()
    ttt.write_travis()


if __name__ == '__main__':
    main()
