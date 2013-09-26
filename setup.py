#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pkgutil import get_importer


# Navigate, import, and retrieve the metadata of the project.
meta = get_importer('src/hocr').find_module('meta').load_module('meta')


setup(
    name='hocr',
    version=meta.version,
    description=meta.description,
    author='Concordus Applications',
    author_email='support@concordusapps.com',
    url='https://github.com/concordusapps/python-hocr',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
    ],
    package_dir={'hocr': 'src/hocr'},
    packages=find_packages('src'),
    entry_points={
        'console_scripts': ['hocr2pdf = hocr.commands:hocr2pdf']
    },
    install_requires=[
        'six',
        'lxml >= 3.2.3, < 4.0.0',
        'hummus >= 0.2.0',
        'python-magic',
        'pillow'
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-pep8',
            'pytest-cov'
        ],
    },
)
