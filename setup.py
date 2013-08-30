#! /usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os import path

# Calculate the base directory of the project to get relatives from.
BASE_DIR = path.abspath(path.dirname(__file__))

setup(
    name='python-hocr',
    version='0.0.0',
    author='Concordus Applications',
    author_email='support@concordusapps.com',
    package_dir={'contracts': 'src/contracts'},
    packages=find_packages(path.join(BASE_DIR, 'src')),
    install_requires=[],
)
