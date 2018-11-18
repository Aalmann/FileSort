from __future__ import print_function
import os
import platform
import subprocess
import shutil
from distutils import dir_util
from FileSort import __version__


def _install_pyinstaller(pyinstaller_path):
    subprocess.call("pip install pyinstaller", shell=True)
    # try to install pyinstaller if not installed
    if not os.path.exists(pyinstaller_path):
        os.mkdir(pyinstaller_path)


def _run_bin(pyinstaller_path):
    # run the binary to test if working
    file_sort_bin = os.path.join(pyinstaller_path, 'dist', 'FileSort',
                                 'FileSort')
    if platform.system() == 'Windows':
        file_sort_bin += '.exe'
    print("Trying to execute %s" % file_sort_bin)
    retcode = os.system(file_sort_bin)
    if retcode != 0:
        raise Exception("Binary not working")


def _windows_version_file(VERSION):
    template = """# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers={version_tuple},
    prodvers={version_tuple},
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x4,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'000004b0',
        [StringStruct(u'Comments', u'This executable was created with pyinstaller'),
        StringStruct(u'CompanyName', u'Alexander Hanl'),
        StringStruct(u'FileDescription', u'File sorter - to sort especially images by their date'),
        StringStruct(u'FileVersion', u'{VERSION}'),
        StringStruct(u'LegalCopyright', u'Copyright 2018 Alexander Hanl'),
        StringStruct(u'ProductName', u'FileSort'),
        StringStruct(u'ProductVersion', u'{VERSION}')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [0, 1200])])
  ]
)"""
    if "-" in VERSION:
        VERSION, _ = VERSION.split("-")
    version_tuple = tuple([int(v) for v in VERSION.split(".")] + [0])
    return template.format(VERSION=VERSION, version_tuple=version_tuple)


def pyinstall(source_folder):
    pyinstaller_path = os.path.join(os.getcwd(), 'pyinstaller')
    _install_pyinstaller(pyinstaller_path)
    command = "pyinstaller"  # "python pyinstaller.py"

    try:
        shutil.rmtree(os.path.join(pyinstaller_path))
    except Exception as e:
        print("Unable to remove old folder", e)

    file_sort_path = os.path.join(source_folder, 'FileSort.py')
    hidden = "--hidden-import=glob"
    if platform.system() != "Windows":
        hidden += " --hidden-import=setuptools.msvc"
        win_ver = ""
    else:
        win_ver_file = os.path.join(pyinstaller_path, 'windows-version-file')
        content = _windows_version_file(__version__)

        def save(path, content):
            """
            Saves a file with given content
            Params:
            path: path to write file to
            load: contents to save in the file
            """
            try:
                os.makedirs(os.path.dirname(path))
            except:
                pass
            with open(path, "wb") as handle:
                try:
                    handle.write(bytes(content, "utf-8"))
                except:
                    handle.write(bytes(content))

        save(win_ver_file, content)
        win_ver = "--version-file %s" % win_ver_file

    if not os.path.exists(pyinstaller_path):
        os.mkdir(pyinstaller_path)
    subprocess.call('%s -y -p %s --console %s %s %s'
                    % (command, source_folder, file_sort_path, hidden, win_ver),
                    cwd=pyinstaller_path, shell=True)

    _run_bin(pyinstaller_path)

    file_sort_bin = os.path.join(pyinstaller_path, 'dist', 'build', 'FileSort')

    return os.path.abspath(os.path.join(pyinstaller_path, 'dist', 'build', 'FileSort'))


if __name__ == "__main__":
    source_folder = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
    output_folder = pyinstall(source_folder)
    print("\n**************FileSort binaries created!******************\n"
          "\nAppend this folder to your system PATH: '%s'\n"
          "Feel free to move the whole folder to another location." % output_folder)
