# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import FileSort

readme_file = open("README.rst", "rt").read()

setup(
    name="FileSort",
    version=FileSort.__version__,
    author="Aalmann",
    author_email="ttt.aalmann@web.de",
    packages=find_packages(),
    scripts=["FileSort.py"],
    url="https://github.com/aalmann/file_sort",
    license="BSD",
    keywords="image sorter based on exif metadata",
    description=" ".join(FileSort.__doc__.splitlines()).strip(),
    long_description=readme_file,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: BSD License",
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
