'''
Created on 18.11.2018

@author: Alex
'''
import os
import shutil
import platform
import requests
import sys
import tarfile


class TestData(object):

    test_data_dir = "test_data"
    sorted_data_dir = "sorted_test_data"

    td_compressed_file = "master.tar.gz"
    td_url = "https://github.com/Aalmann/FileSort_testdata/archive/%s" % td_compressed_file

    @staticmethod
    def assure_test_data():
        if not os.path.exists(TestData.test_data_dir):
            TestData.download_extract()

    @staticmethod
    def download_extract():
        if os.path.exists(TestData.test_data_dir):
            shutil.rmtree(TestData.test_data_dir, ignore_errors=False, onerror=None)
        if os.path.exists(TestData.sorted_data_dir):
            shutil.rmtree(TestData.sorted_data_dir, ignore_errors=False, onerror=None)
        if os.path.exists(TestData.td_compressed_file):
            os.remove(TestData.td_compressed_file)

        print("Trying to download test data.")
        res = requests.get(TestData.td_url, stream=True)
        total_length = res.headers.get('content-length')
        if total_length:
            total_length = int(total_length)

        last_out = ""
        if res.status_code == 200:
            dl = 0
            with open(TestData.td_compressed_file, 'wb') as f:
                for chunk in res.iter_content(1024):
                    f.write(chunk)
                    dl += len(chunk)
                    if total_length:
                        done = int(50 * dl / total_length)
                        out = "\r[%s%s]" % ('=' * done, ' ' * (50 - done))
                        if out != last_out:
                            sys.stdout.write(out)
                            last_out = out
                    else:
                        # sys.stdout.write("\r %s" % dl)
                        pass
                    sys.stdout.flush()
        print("")

        print("Extracting test data")
        if TestData.td_compressed_file.endswith(".tar.gz"):
            tar = tarfile.open(TestData.td_compressed_file, "r:gz")
            tar.extractall(path=TestData.test_data_dir)
            tar.close()


class FileSortHelper(object):

    @staticmethod
    def _get_file_sort_cmd():
        fs_path = None
        if platform.system() == 'Windows':
            fs_ext = ".exe"
        else:
            fs_ext = ""
        fs_name = "FileSort"
        the_paths = os.environ.get("PATH").split(os.pathsep)
        for p in the_paths:
            fs_p = os.path.join(p, fs_name + fs_ext)
            if os.path.exists(fs_p):
                fs_path = fs_p
                break

        return fs_path

    @staticmethod
    def call_File_Sort(args):
        if not isinstance(args, list):
            args = [args]
        fs_cmd = FileSortHelper._get_file_sort_cmd()
        if fs_cmd and os.environ.get("FILE_SORT_TEST_EXECUTABLE"):
            args = [fs_cmd] + args
            print(">>> Calling: %s" % (args))
            ret_val = os.system(" ".join(args))
        else:
            from FileSort import main
            args = ["FileSort.py"] + args
            print(">>> Calling: %s" % (args))
            try:
                ret_val = main(args)
            except SystemExit as sys_ex:
                ret_val = sys_ex.code

        print(ret_val)
        return ret_val
