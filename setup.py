#  Copyright (C) 2014 Jump Operations, LLC
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to:
#    Free Software Foundation, Inc.
#    51 Franklin Street, Fifth Floor
#    Boston, MA  02110-1301, USA.


import os
from setuptools import setup

import attask

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pyattask",
    version = attask.__version__,
    author = "David Ressman",
    author_email = "davidr@ressman.org",
    description = ("Python bindings for the AtTask API"),
    license = "GPLv2",
    keywords = "attask api bindings",
    packages=['attask'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
)


