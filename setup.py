#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='flask_debugtoolbar_flamegraph',
    version='0.1.0',
    description='Flamegraphs for Flask Debug Toolbar',
    long_description=readme,
    author='Pekka Pöyry',
    author_email='pekka.poyry@gmail.com',
    url='https://github.com/quantus/flask-debugtoolbar-flamegraph',
    packages=[
        'flask_debugtoolbar_flamegraph',
    ],
    package_dir={'flask_debugtoolbar_flamegraph':
                 'flask_debugtoolbar_flamegraph'},
    license='MIT',
    zip_safe=False,
    include_package_data=True,
    keywords='flask_debugtoolbar_flamegraph',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ]
)
