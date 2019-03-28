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
    requirements = requirements_file.readlines()

test_requirements = [
    'pytest', 'coverage', 'flake8'
]


# Cribbed from https://github.com/pypa/setuptools/issues/1052
def get_requirements(remove_links=True):
    """
    lists the requirements to install.
    """
    requirements = []
    try:
        with open('requirements.txt') as f:
            requirements = f.read().splitlines()
    except Exception as ex:
        with open('aguamenti.egg-info\requires.txt') as f:
            requirements = f.read().splitlines()
    if remove_links:
        for requirement in requirements:
            # git repository url.
            if requirement.startswith("git+"):
                requirements.remove(requirement)
            # subversion repository url.
            if requirement.startswith("svn+"):
                requirements.remove(requirement)
            # mercurial repository url.
            if requirement.startswith("hg+"):
                requirements.remove(requirement)
    return requirements


def get_links():
    """
    gets URL Dependency links.
    """
    links_list = get_requirements(remove_links=False)
    for link in links_list:
        keep_link = False
        already_removed = False
        # git repository url.
        if not link.startswith("git+"):
            if not link.startswith("svn+"):
                if not link.startswith("hg+"):
                    links_list.remove(link)
                    already_removed = True
                else:
                    keep_link = True
                if not keep_link and not already_removed:
                    links_list.remove(link)
                    already_removed = True
            else:
                keep_link = True
            if not keep_link and not already_removed:
                links_list.remove(link)
    return links_list

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
    install_requires=get_requirements(),
    dependency_links=get_links(),
    license="BSD",
    zip_safe=False,
    keywords='aguamenti',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points = {
        'console_scripts':  [
            'aguamenti = aguamenti.commandline:cli'
        ]
    },
    test_suite='tests',
    tests_require=test_requirements
)
