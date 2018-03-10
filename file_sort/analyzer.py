'''
Created on 04.03.2018

@author: Alex
'''

import os
import json
import logging

from datetime import datetime
import re
import exifread

from file_sort import FileSortException


class Analyzer(object):
    '''
    Analyzes the files by their date and writes a file.
    '''

    class MappingResult(object):

        SETTINGS_FILE_NAME = "settings.filesort"
        FILES_FILE_NAME = "files.filesort"

        def __init__(self):
            # self._settings = {"modes": ["exif", "file_date"]}
            self._settings = {"modes": "exif"}
            self._files = []
            pass

        def load(self, settings_filename, files_filename):
            with open(settings_filename, "r") as f:
                ds = json.load(f, encoding='cp1250')
                self._settings = ds.get("settings")
            with open(files_filename, "r") as f:
                df = json.load(f, encoding='cp1250')
                self._files = df.get("files")

        def save(self, settings_filename, files_filename):
            ds = {"settings": self._settings}
            df = {"files": self._files}
            with open(settings_filename, "w") as f:
                json.dump(ds, f, encoding='cp1250', indent=4)
            with open(files_filename, "w") as f:
                json.dump(df, f, encoding='cp1250', indent=4)

    def __init__(self, directory, recurse=True):
        '''
        Constructor
        :param directory of the files
        :param recurse, if True the directory will be processed recursive
        '''
        self._directory = directory
        self._recurse = recurse
        self._mapping = self.MappingResult()
        self._settings_file = os.path.join(directory,
                                           self.MappingResult.
                                           SETTINGS_FILE_NAME)
        self._files_file = os.path.join(directory,
                                        self.MappingResult.FILES_FILE_NAME)
        if os.path.exists(self._settings_file):
            logging.info("Using existing settings file: %s" %
                         self._settings_file)
            self._load_mapping()
        else:
            logging.info("Creating a new default settings file.")
            self._create_default_mapping()

    def analyze(self):
        self._mapping._files = []
        for root, dirs, files in os.walk(self._directory):
            for name in files:
                file_name = os.path.join(root, name)
                file_base = os.path.basename(file_name)
                ext = file_name.split(".")[-1:][-1]
                if file_name in [self._settings_file, self._files_file]:
                    continue
                if ext.lower() in ['jpg', 'jpeg', 'mp4', 'mpg', 'mpeg',
                                   'mov', 'gif', '3gp', 'avi', 'wmv',
                                   'lrv', 'png', 'pdf', 'enc', 'nomedia',
                                   'thm']:
                    d = {}
                    d["old_file_path"] = file_name
                    logging.debug("analyzing: " + file_name)
                    exif_date = self._get_exif_date(file_name)
                    d["exif_date"] = str(exif_date)
                    file_attr_mod = self._get_file_attrib_date(file_name,
                                                               "modified_time")
                    d["file_attr_mod"] = str(file_attr_mod)
                    file_attr_create = self._get_file_attrib_date(
                                                file_name,
                                                "creation_time")
                    d["file_attr_create"] = str(file_attr_create)
                    file_name_date = self._get_file_name_date(file_base)
                    d["file_name_date"] = str(file_name_date)
                    best_matching_date = self._get_best_matching_date(
                                                exif_date,
                                                file_attr_mod,
                                                file_attr_create,
                                                file_name_date)
                    d["best_matching_date"] = str(best_matching_date)
                    new_file_path = self._get_new_file_path(file_base,
                                                            best_matching_date)
                    d["new_file_path"] = new_file_path
                    self._mapping._files.append(d)
                else:
                    logging.info("Skipping unknown file format for file: " +
                                 file_name)

            for name in dirs:
                logging.info("Processing directory: " +
                             os.path.join(root, name))
        self._mapping.save(self._settings_file, self._files_file)
        pass

    def _get_new_file_path(self, file_base, best_matching_date):
        path = os.path.join(self._directory,
                            "_sorted",
                            best_matching_date.strftime("%Y"),
                            best_matching_date.strftime("%B"),
                            file_base)
        return path

    def _get_best_matching_date(self, exif_date, file_attr_mod,
                                file_attr_create, file_name_date):
        if exif_date:
            return exif_date
        elif file_name_date:
            return file_name_date
        elif file_attr_create < file_attr_mod:
            return file_attr_create
        else:
            return file_attr_mod

    def _get_exif_date(self, file_name):
        with open(file_name, "rb") as f:
            # stop_tag="EXIF DateTimeOriginal",
            tag = exifread.process_file(f, details=False)
            result = tag.get("EXIF DateTimeOriginal") or \
                tag.get("Image DateTime") or None
            if result:
                try:
                    result = datetime.strptime(str(result),
                                               "%Y:%m:%d %H:%M:%S")
                except Exception:
                    result = datetime.strptime(str(result),
                                               "%d/%m/%Y %H:%M")
            return result

    def _get_file_attrib_date(self, file_name, date_type):

        if date_type == "creation_time":
            return datetime.fromtimestamp(os.path.getctime(file_name))
        elif date_type == "modified_time":
            return datetime.fromtimestamp(os.path.getmtime(file_name))
        else:
            raise FileSortException("Unknown date_type used \
                                    for file attribute.")

    def _get_file_name_date(self, file_base):
        file_name_date = None
        # at first try to find a date with YYYY MM DD with
        # separator -._ or without
        result = re.search(
            "([1][9][7-9]\d{1}|[2][0]\d{2})([\-\.\_]\
            {0,1})(\d{2})([\-\.\_]{0,1})(\d{2})",
            file_base)
        if result and str(result) != "null":
            # group 0 contains the complete match, so we take 1, 3 and 5
            file_name_date = result.group(1) + "-" + \
                result.group(3) + "-" + \
                result.group(5)
        else:
            # at first try to find a date with DD MM YYYY with
            # separator -._ or without
            result = re.search(
                "(\d{2})([\-\.\_]{0,1})(\d{2})([\-\.\_]\
                {0,1})([1][9][7-9]\d{1}|[2][0]\d{2})",
                file_base)
            if result and str(result) != "null":
                # again group 0 contains the complete match,
                # so we take 5, 3 and 1
                file_name_date = result.group(5) + "-" + \
                    result.group(3) + "-" + \
                    result.group(1)
        the_date = None
        if file_name_date:
            # now try to create a valid date object
            try:
                the_date = datetime.strptime(file_name_date, "%Y-%m-%d")
            except Exception:
                # date can't be created, let's try another format
                the_date = datetime.strptime(file_name_date, "%Y-%d-%m")
        return the_date if the_date else None

    def _load_mapping(self):
        self._mapping.load(self._settings_file, self._files_file)
        pass

    def _create_default_mapping(self):
        self._mapping.save(self._settings_file, self._files_file)

        pass
