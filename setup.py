# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os.path

readme = ''
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, 'README.rst')
if os.path.exists(readme_path):
    with open(readme_path, 'rb') as stream:
        readme = stream.read().decode('utf8')

setup(
    long_description=readme,
    name='dephell',
    version='0.7.4',
    description='Dependency resolution for Python',
    python_requires='>=3.5',
    project_urls={
        'repository': 'https://github.com/dephell/dephell',
        'documentation': 'https://dephell.readthedocs.io/en/latest/'
    },
    author='Gram',
    author_email='master_fess@mail.ru',
    license='MIT',
    keywords='dephell packaging dependency dependencies venv licenses pip poetry pipfile pipenv setuptools',
    classifiers=[
        'Development Status :: 4 - Beta', 'Environment :: Console',
        'Framework :: Setuptools Plugin', 'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python', 'Topic :: Security',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points={'console_scripts': ['dephell = dephell.cli:entrypoint']},
    packages=[
        'dephell', 'dephell.actions', 'dephell.commands', 'dephell.config',
        'dephell.controllers', 'dephell.converters', 'dephell.models',
        'dephell.repositories', 'dephell.repositories._conda',
        'dephell.repositories._git', 'dephell.repositories._warehouse'
    ],
    package_data={'dephell': ['templates/*.j2']},
    install_requires=[
        'aiohttp', 'appdirs', 'attrs', 'cerberus>=1.3',
        'dephell-archive>=0.1.5', 'dephell-discover>=0.2.6',
        'dephell-licenses>=0.1.6', 'dephell-links>=0.1.4',
        'dephell-markers>=0.2.6', 'dephell-pythons>=0.1.11',
        'dephell-shells>=0.1.3', 'dephell-specifier>=0.1.7',
        'dephell-venvs>=0.1.16', 'html5lib', 'jinja2', 'm2r', 'packaging',
        'pip>=18.0', 'pyyaml', 'requests', 'setuptools', 'tomlkit', 'yaspin'
    ],
    extras_require={
        'full': ['aiofiles', 'autopep8', 'colorama', 'graphviz', 'yapf'],
        'dev': [
            'aioresponses', 'pygments-github-lexers', 'pytest', 'recommonmark',
            'requests-mock', 'sphinx', 'sphinx-rtd-theme'
        ],
        'tests': ['aioresponses', 'pytest', 'requests-mock'],
        'docs': [
            'pygments-github-lexers', 'recommonmark', 'sphinx',
            'sphinx-rtd-theme'
        ]
    },
)
