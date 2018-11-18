# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from FileSort import __doc__ as fs_doc
from FileSort import __version__ as fs_version

README_FILE = open("README.rst", "rt").read()
VERSION = fs_version
DOC = fs_doc

setup(
    name="FileSort",
    version=VERSION,
    author="Aalmann",
    author_email="ttt.aalmann@web.de",
    packages=find_packages(),
    scripts=["FileSort.py"],
    url="https://github.com/aalmann/file_sort",
    license="MIT",
    keywords="image sorter based on exif metadata",
    description=" ".join(DOC.splitlines()).strip(),
    long_description=README_FILE,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Utilities",
    ],
    entry_points={
        'console_scripts': [
            'FileSort=FileSort:run'
        ],
    },
)
