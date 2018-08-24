#! /usr/bin/env python

import os
import time
import re
import locale
import subprocess
import zipfile
import glob

import private.metadata as metadata
import private.messages as messages

from private.exceptionclasses import CustomError, CritError, SyntaxError, LogicError
from private.utility import norm_path


def delete_files(path):
    path = norm_path(path)
    print("\nDeleted:", path)

    for f in glob.glob(path):
        os.remove(f)


def remove_dir(path, option = ''):
    path = norm_path(path)
    if not option:
        option = metadata.default_options[os.name]['rmdir']

    command = metadata.commands[os.name]['rmdir'] % (option, path)
    subprocess.check_call(command.split())
    

def clear_dirs(*args):
    for path in args:
        if os.path.isdir(path):
            remove_dir(path)
        
        os.makedirs(path)
        
        print('Cleared: "%s"' % path)


def unzip(file_name, output_dir):
    zip = zipfile.ZipFile(file_name, allowZip64=True)
    zip.extractall(output_dir)
    zip.close()


def zip_dir(source_dir, dest):
    zf = zipfile.ZipFile('%s.zip' % (dest), 'w', zipfile.ZIP_DEFLATED, allowZip64=True)
    abs_src = os.path.abspath(source_dir)
    for dirname, subdirs, files in os.walk(source_dir):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print 'zipping %s as %s' % (os.path.join(dirname, filename), arcname)
            zf.write(absname, arcname)
    zf.close()

