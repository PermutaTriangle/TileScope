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
    install_requires=read("requirements.txt").splitlines(),
    packages=find_packages(),
    long_description=read("README.md"),
)
