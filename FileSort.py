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

import sys
import os

import logging

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from file_sort.analyzer import Analyzer
from file_sort.copy import Copy

__all__ = []
__version__ = '0.2.0'
__date__ = '2018-03-05'
__updated__ = '2018-11-18'

DEBUG = 0
TESTRUN = 0
PROFILE = 0


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''

    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def main(argv=None):
    '''
    Command line options.
    '''
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version,
                                                     program_build_date)
    program_shortdesc = __doc__.split("\n")[1]
    program_license = '''%s

  Created by Alexander Hanl (Aalmann) on %s (last update %s).
  Copyright 2018. All rights reserved.

  Licensed under MIT License

USAGE
''' % (program_shortdesc, str(__date__), str(__updated__))

    if len(argv) <= 1:
        argv.append("--help")

    try:
        command = argv[1]
        if command == "analyze":
            # Setup argument parser
            parser = ArgumentParser(description=program_license,
                                    formatter_class=RawDescriptionHelpFormatter,
                                    prog="FileSort analyze")
            parser.add_argument("-r", "--recursive", dest="recurse",
                                action="store_true",
                                help="recurse into subfolders [default: %(default)s]")
            # parser.add_argument("-v", "--verbose", dest="verbose",
            # action="count", help="set verbosity level [default: %(default)s]")

            parser.add_argument(dest="directory",
                                help="paths to directory with files",
                                metavar="directory", nargs='?')

            # Process arguments
            args = parser.parse_args(argv[2:])

            if not args.directory:
                parser.print_help()
                logging.error("directory not set.")
                print("\nERROR: directory not set")
                parser.print_usage()
                return 1
            logging.info("Using directory %s" % (args.directory))
            directory = args.directory
            # verbose = args.verbose
            recurse = args.recurse

            analyzer = Analyzer(directory, recurse)
            analyzer.analyze()

            # if verbose > 0:
            #    print("Verbose mode on")
            #    if recurse:
            #        print("Recursive mode on")
            #    else:
            #        print("Recursive mode off")
        elif command == "copy":
            # Setup argument parser
            parser = ArgumentParser(description=program_license,
                                    formatter_class=RawDescriptionHelpFormatter,
                                    prog="FileSort copy")
            # parser.add_argument("-v", "--verbose", dest="verbose",
            # action="count", help="set verbosity level [default: %(default)s]")

            parser.add_argument(dest="directory",
                                help="paths to directory with files",
                                metavar="directory", nargs='?')

            # Process arguments
            args = parser.parse_args(argv[2:])

            if not args.directory:
                parser.print_help()
                logging.error("directory not set.")
                print("\nERROR: directory not set")
                parser.print_usage()
                return 1
            logging.info("Using directory %s" % (args.directory))
            directory = args.directory
            # verbose = args.verbose

            copier = Copy(directory)
            copier.copy()

        elif command in ["--help", "-h", "help"]:
            # Setup argument parser
            commd_help = "\nThe following commands are available:"
            commd_help += "\n    help       print this help message"
            commd_help += "\n    analyze    \
            Analyze a directory and create a mapping file for copy or move \
            command."
            commd_help += "\n    copy       Copies the files listed in mapping \
            file to the analyzed destinations"
            commd_help += "\n    move       Moves the files listed in mapping \
            file to the analyzed destination"
            commd_help += "\n    revert     Tries to reverts the changes from \
            move command."
            parser = ArgumentParser(description=program_license + commd_help,
                                    formatter_class=RawDescriptionHelpFormatter,
                                    prog="FileSort")
            parser.add_argument("command", help="Command to be executed",
                                nargs="?")
            parser.add_argument('-v', '--version', action='version',
                                version=program_version_message)

            # Process arguments
            args = parser.parse_args()
        elif command == "-v" or command == "--version":
            parser = ArgumentParser(description=program_license,
                                    formatter_class=RawDescriptionHelpFormatter,
                                    prog="FileSort")
            parser.add_argument('-v', '--version', action='version',
                                version=program_version_message)
            # Process arguments
            args = parser.parse_args()
        return 0
    except KeyboardInterrupt:
        # handle keyboard interrupt
        return 0
    except Exception as exc:
        if DEBUG or TESTRUN:
            raise(exc)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(exc) + "\n" +
                         exc.msg + "\n")
        import traceback
        sys.stderr.write(traceback.format_exc())
        sys.stderr.write(indent + "  for help use --help")
        return 2


def run():
    # main(sys.argv[1:])
    return main()


if __name__ == "__main__":
    '''
    Bla
    bli
    '''
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
        sys.argv.append("-r")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'file_sort.FileSort_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)

    sys.exit(main())
