# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from FileSort import __doc__ as fs_doc
from FileSort import __version__ as fs_version

README_FILE = open("README.rst", "rt").read()
VERSION = fs_version
DOC = fs_doc


def read_requirements(req_filename):
    reqs = []
    with open(req_filename, "rt") as req_file:
        for line in req_file.read().splitlines():
            if not line.strip().startswith("#"):
                reqs.append(line)
    return reqs


setup(
    name="FileSort",
    version=VERSION,
    author="Aalmann",
    author_email="ttt.aalmann@web.de",
    scripts=["FileSort.py"],
    url="https://github.com/aalmann/file_sort",
    license="MIT",
    keywords="image sorter based on exif metadata",
    description=" ".join(DOC.splitlines()).strip(),
    long_description=README_FILE,
    install_requires=read_requirements('file_sort/requirements.txt'),
    packages=find_packages(exclude="test"),
    package_data={
        'file_sort': ['*.txt'],
    },
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
