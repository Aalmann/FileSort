*******
FileSort.py
*******

.. image:: https://travis-ci.org/Aalmann/FileSort.svg?branch=master
    :target: https://travis-ci.org/Aalmann/FileSort

.. image:: https://codecov.io/gh/Aalmann/FileSort/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/Aalmann/FileSort

Easy to use Python module to sort files based on their Exif metadata (if it's an image) or file attributes.


Installation
************

PyPI
====
It is recommended to install the `PyPI package <https://pypi.python.org/pypi/FileSort>`_,
using pip or easy_install to get latest and greatest version::

    $ pip install FileSort

See the `pip documentation <https://pip.pypa.io/en/latest/user_guide.html>`_ for more info.

Archive
=======
You can download an archive from the project's `releases page <https://github.com/aalmann/FileSort/releases>`_.

Extract and enjoy.


Compatibility
*************

FileSort.py is tested on the following Python versions:

- 2.7
- 3.6
- 3.7


Usage
*****

Command line
============

Some examples::

    $ FileSort.py analyze <input files directory>
    $ FileSort.py copy <input files directory>

Show command line options::

    $ FileSort.py --help

