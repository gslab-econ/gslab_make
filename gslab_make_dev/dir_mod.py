#! /usr/bin/env python

import os
import time
import traceback
import re
import locale
import subprocess
import zlib
import zipfile

import private.metadata as metadata
import private.messages as messages
from glob import glob
from private.exceptionclasses import CustomError, CritError, SyntaxError, LogicError
from private.preliminaries import print_error


#== Directory modification functions =================
def delete_files(pathname):
    """Delete files specified by a path

    This function deletes a possibly-empty list of files whose names match 
    `pathname`, which must be a string containing a path specification. 
    `pathname` can be either absolute (like /usr/src/Python-1.5/Makefile) 
    or relative (like ../../Tools/*/*.gif). It can contain shell-style wildcards.
    """
    print("\nDelete files", pathname)

    for f in glob(pathname):
        os.remove(f)


def remove_dir(pathname, options = '@DEFAULTVALUE@'):
    """Remove a directory

    This function completely removes the directory specified by `pathname` 
    using the 'rmdir' command on Windows platforms and the 'rm' command 
    on Unix platforms. This is useful for removing symlinks without 
    deleting the source files or directory.
    """

    if os.name == 'posix':
        os_command = 'rmdirunix'
        if pathname[-1] == '/':
            pathname = pathname[0:-1]
    else:
        os_command = 'rmdirwin'

    command = metadata.commands[os_command]
    if options == '@DEFAULTVALUE@':
        options = metadata.default_options[os_command]

    subprocess.check_call(command % (options, pathname), shell=True)



def list_directory(top, makelog = '@DEFAULTVALUE@'):
    """List directories

    This function lists all non-hidden sub-directories of the directory
    specified by `top`, a path, and their content from the top down.
    It writes their names, modified times, and sizes in bytes to the 
    log file specified by the path `makelog`.
    """

    # metadata.settings should not be part of argument defaults so that they can be
    # overwritten by make_log.set_option
    if makelog == '@DEFAULTVALUE@':
        makelog = metadata.settings['makelog_file']

    print("\nList all files in directory", top)

    # To print numbers (file sizes) with thousand separator
    locale.setlocale(locale.LC_ALL, '')

    makelog = re.sub('\\\\', '/', makelog)
    try:
        LOGFILE = open(makelog, 'ab')
    except Exception as errmsg:
        print errmsg
        raise CritError(messages.crit_error_log % makelog)

    print >> LOGFILE, '\n'
    print >> LOGFILE, 'List of all files in sub-directories in', top

    try:
        if os.path.isdir(top):
            for root, dirs, files in os.walk(top, topdown = True):
                # Ignore non-hidden sub-directories
                dirs_to_keep = []
                for dirname in dirs:
                    if not dirname.startswith('.'):
                        dirs_to_keep.append(dirname)
                dirs[:] = dirs_to_keep

                # Print out the sub-directory and its time stamp
                created = os.stat(root).st_mtime
                asciiTime = time.asctime(time.localtime(created))
                print >> LOGFILE, root
                print >> LOGFILE, 'created/modified', asciiTime

                # Print out all the files in the sub-directories
                for name in files:
                    full_name = os.path.join(root, name)
                    created = os.path.getmtime(full_name)
                    size = os.path.getsize(full_name)
                    asciiTime = time.asctime(time.localtime(created))
                    print >> LOGFILE, '%50s' % name, '--- created/modified', asciiTime, \
                        '(', locale.format('%d', size, 1), 'bytes )'
    except:
        print_error(LOGFILE)

    print >> LOGFILE, '\n'
    LOGFILE.close()


def clear_dirs(*args):
    """Create fresh directories

    This function creates a directory for each path specified in 
    *args if such a directory does not already exist. It deletes
    all files in each directory that already exists while keeping 
    directory structure (i.e. sub-directories). This function is
    safe for symlinks.
    """
    for dir in args:
        if os.path.isdir(dir):
            remove_dir(dir)
        os.makedirs(dir)
        print 'Cleared:', dir


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

