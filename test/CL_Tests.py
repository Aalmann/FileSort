'''
Created on 04.11.2018

@author: Alex
'''
import unittest

from .test_helper import TestData, FileSortHelper


class TestCommandLine(unittest.TestCase):

    def setUp(self):
        TestData.assure_test_data()
        pass

    def tearDown(self):
        pass

    def test_1_help_1(self):
        self.assertEqual(FileSortHelper.call_File_Sort(["-h"]), 0)

    def test_1_help_2(self):
        self.assertEqual(FileSortHelper.call_File_Sort(["--help"]), 0)

    def test_2_analyze_1(self):
        self.assertEqual(FileSortHelper.call_File_Sort(["analyze"]), 1)

    def test_2_analyze_2(self):
        self.assertEqual(FileSortHelper.call_File_Sort(["analyze", "-h"]), 0)

    def test_2_analyze_3(self):
        self.assertEqual(FileSortHelper.call_File_Sort(["analyze", TestData.test_data_dir]), 0)

    def test_3_copy_1(self):
        self.assertEqual(FileSortHelper.call_File_Sort(["copy", TestData.test_data_dir]), 0)


if __name__ == "__main__":
    TestData.download_extract()
    # import sys;sys.argv = ['', 'TestCommandLine.testName']
    unittest.main()
