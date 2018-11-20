#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read()

test_requirements = [
    'pytest', 'coverage'
]

setup(
    name='aguamenti',
    version='0.1.0',
    description="Python utility scripts for working with reflow workflows. "
                "\"Aguamenti\" is a spell in Harry Potter that creates water "
                "out of nothing.",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    author="Olga Botvinnik",
    author_email='olga.botvinnik@gmail.com',
    url='https://github.com/czbiohub/aguamenti',
    packages=[
        'aguamenti',
    ],
    package_dir={'aguamenti':
                 'aguamenti'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='aguamenti',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
