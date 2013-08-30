#! /usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='python-hocr',
    version='0.0.0',
    author='Concordus Applications',
    author_email='support@concordusapps.com',
    package_dir={'contracts': 'src/contracts'},
    packages=find_packages('src'),
    install_requires=[],
    extras_require={
        'test': [
            'pytest'
        ],
    },
)
