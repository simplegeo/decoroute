#!/usr/bin/env python
#
# $Id: setup.py,v 7027370799fe 2009/10/28 07:01:52 vsevolod $

from setuptools import setup

import decoroute

setup(
    name='decoroute',
    version=decoroute.__version__,
    description="Pattern-matching based WSGI-compliant URL routing tool",
    long_description=open('README.txt').read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Natural Language :: Russian",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ], 
    keywords='python wsgi decorator route routing tool mvc mtv web webdev www',
    author='Vsevolod Balashov',
    author_email='vsevolod@balashov.name',
    url='http://pypi.python.org/pypi/decoroute',
    license='LGPL 2.1',
    py_modules=["decoroute"],
    test_suite='nose.collector',
    zip_safe=True
)
