#! /usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='python-hocr',
    version='0.0.0',
    author='Concordus Applications',
    author_email='support@concordusapps.com',
    package_dir={'hocr': 'src/hocr'},
    packages=find_packages('src'),
    install_requires=[
        'lxml >= 3.2.3, < 4.0.0'
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-pep8',
            'pytest-cov'
        ],
    },
)
