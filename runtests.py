#!/usr/bin/env python
import pytest
import os
import sys


os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'


# Adding current directory to ``sys.path``.
parent = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, parent)


def runtests(*argv):
    argv = list(argv) or [
        'tests',
    ]
    pytest.main(argv)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
