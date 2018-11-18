#!/usr/bin/python3
# encoding: utf-8
'''
FileSort -- Sorts files based on their EXIF data or file date.

FileSort is a Python program to sort files based on their EXIF or
file date.

It defines classes_and_methods

@author:     Alexander Hanl (Aalmann)

@copyright:  2018. All rights reserved.

@license:    MIT

@deffield    updated: Updated
'''

from file_sort.fs_main import main as fs_main, run as fs_run


def run():
    # main(sys.argv[1:])
    return fs_run()


if __name__ == "__main__":
    '''
    main
    '''
    import sys
    sys.exit(fs_main())
