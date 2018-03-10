'''
Created on 04.03.2018

@author: Alex
'''

import os
import json
import logging
import shutil

from file_sort import FileSortException


class Copy(object):
    '''
    Copies the files which are listet in the files.filesort
    '''

    class MappingResult(object):

        FILES_FILE_NAME = "files.filesort"

        def __init__(self):
            # self._settings = {"modes": ["exif", "file_date"]}
            self._settings = {"modes": "exif"}
            self._files = []
            pass

        def load(self, files_filename):
            with open(files_filename, "r") as f:
                df = json.load(f, encoding='cp1250')
                self._files = df.get("files")

    def __init__(self, directory):
        '''
        Constructor
        :param directory of the files
        '''
        self._directory = directory
        self._mapping = self.MappingResult()
        self._files_file = os.path.join(directory,
                                        self.MappingResult.FILES_FILE_NAME)
        if os.path.exists(self._files_file):
            logging.info("Processing file: %s" % self._files_file)
            self._load_files()
        else:
            raise FileSortException("No %s found in %s.\nRun analyze command \
                        first." % (self._files_file, self._directory))

    def copy(self):
        for the_file in self._mapping._files:
            old_path = the_file.get("old_file_path")
            new_path = the_file.get("new_file_path")
            if os.path.exists(new_path):
                logging.warn(
                    "File %s already exists. Will copy it to _file_sort_twins \
                    in %s." % (new_path, self._directory))
                new_path = new_path.replace("_sorted", "_file_sort_twins")
            if not os.path.exists(os.path.dirname(new_path)):
                os.makedirs(os.path.dirname(new_path))
            old_short = old_path.replace(self._directory, "")
            new_short = new_path.replace(self._directory, "")
            logging.info("Copying %s --> %s" % (old_short, new_short))
            shutil.copy2(old_path, new_path)
        pass

    def _load_files(self):
        self._mapping.load(self._files_file)
        pass
