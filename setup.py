#!/usr/bin/env python

from __future__ import print_function
from setuptools import setup, find_packages

from egor.config import VERSION

DEPENDENCIES = [
    'knack',
    'urllib3'
]

with open('README.md', 'r', encoding='utf-8') as f:
    README = f.read()

setup(
    name='egor',
    version=VERSION,
    description='A Task automation tool for competitive programmers',
    long_description=README,
    license='MIT',
    author='Cheracher Mehdi',
    author_email='mehdi.cheracher@gmail.com',
    url='https://github.com/chermehdi/egor',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Competitive programmers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: MIT License',
    ],
    packages=find_packages(),
    package_data={'': ['*.cpp', '*.java']},
    install_requires=DEPENDENCIES,
    extras_require={
        ':python_version<"3.4"': ['enum34']
    },
    entry_points={
        'console_scripts': ['egor=egor:launch']
    }
)
