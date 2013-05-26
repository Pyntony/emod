#!/usr/bin/env python
import sys
from distutils.core import setup

sys.path.insert(0, 'src')
from emod import package_version

setup(
    name = "emod",
    version = package_version,
    package_dir = {'': 'src'},
    packages = ['emod'],
    scripts = ["emod"],
    description = "portage package.* file manager.",
    author = "Antoine Pinsard, Axujen",
    author_email = "A. Pinsard <antoine.pinsard@member.fsf.org>, Axujen <axujen@gmail.org>",
    url = "https://github.com/Pyntony/emod",
    keywords = ["portage", "package"],
	classifiers = [
                'Development Status :: 4 - Beta',
                'Environment :: Console',
                'Intended Audience :: System Administrators',
                'Programming Language :: Python',
                'Topic :: System :: Installation/Setup'
                ],
    long_description = """\
emod
----
emod is a script that make managing /etc/portage/package.* file simply and easy.

features is modifying rules on in package files on the fly and convertion from
directory style package structure to one files and vice versa.
"""
)
