#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='elegion_djangodash2013',
    version='0.0.1',
    description='Django Dash 2013 entry for team e-Legion.',
    author='e-Legion',
    author_email='pr@e-legion.com',
    url='http://www.e-legion.com/',
    packages=[
        'wtl',
        'wtl.wtlib',
    ],
    install_requires=[
        'django==1.5.4',
        'south==0.8.2',
        'nose==1.3.0',
        'django-nose==1.2',
    ],
    zip_safe=False,
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
    ),
)
