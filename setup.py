#!/usr/bin/env python
import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="tilescope_three",
    version="0.0.1",
    author="Henning Ulfarsson",
    author_email="henningu@ru.is",
    maintainer="Christian Nathaniel Bean",
    maintainer_email="christianbean@ru.is",
    url="https://github.com/PermutaTriangle/tilescope_three",
    packages=find_packages(),
    long_description=read("README.md"),
    install_requires=[
        'permuta==1.1.0',
        'comb_spec_searcher==0.2.1',
        'logzero==1.5.0',
        'tilings==1.0.1',
        'sympy==1.4',
    ],
    setup_requires=['pytest-runner==5.1'],
    tests_require=[
        'pytest==5.1.1',
    ],
)
