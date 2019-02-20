#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

######################################################
# Define metadata
######################################################  

makelog_started = False

# Commands
commands = {
    'posix': 
        {'makelink'  : 'ln -s \"%s\" \"%s\"', 
         'rmdir'     : 'rm %s \"%s\"', 
         'stata'     : '%s %s do \\\"%s\\\"',
         'matlab'    : '%s %s -r \"try run(\'%s\'); catch e, fprintf(getReport(e)), exit(1); end; exit(0)\" -logfile \"%s\"',
         'perl'      : '%s %s \"%s\" %s',
         'python'    : '%s %s \"%s\" %s',
         'math'      : '%s < \"%s\" %s',
         'st'        : '%s \"%s\"',
         'lyx'       : '%s %s \"%s\"',
         'r'         : '%s %s \"%s\"',
         'sas'       : '%s %s -log -print %s'},
    'nt': 
        {'makelink'  : 'mklink %s \"%s\" \"%s\"', 
         'rmdir'     : 'rmdir %s \"%s\"', 
         'stata'     : '%s %s do \\\"%s\\\"',
         'matlab'    : '%s %s -r \"try run(\'%s\'); catch e, fprintf(getReport(e)), exit(1); end; exit(0)\" -logfile \"%s\"',
         'perl'      : '%s %s \"%s\" %s',
         'python'    : '%s %s \"%s\" %s',
         'math'      : '%s < \"%s\" %s',
         'st'        : '%s \"%s\"',
         'lyx'       : '%s %s \"%s\"',
         'r'         : '%s %s \"%s\"',
         'sas'       : '%s %s -log -print %s'}
}

default_options = {
    'posix': 
        {'rmdir'     : '-rf', 
         'stata'     : '-e',
         'matlab'    : '-nosplash -nodesktop',
         'perl'      : '',
         'python'    : '',
         'math'      : '-noprompt',
         'st'        : '',
         'lyx'       : '-e pdf2',
         'r'         : '--no-save',
         'sas'       : ''},
    'nt': 
        {'rmdir'     : '/s /q', 
         'stata'     : '/e',
         'matlab'    : '-nosplash -minimize -wait',
         'perl'      : '',
         'python'    : '',
         'math'      : '-noprompt',
         'st'        : '',
         'lyx'       : '-e pdf2',
         'r'         : '--no-save',
         'sas'       : '-nosplash'}
}

default_executables = {
    'posix': 
        {'stata'     : 'stata-mp',
         'matlab'    : 'matlab',
         'perl'      : 'perl',
         'python'    : 'python',
         'math'      : 'math',
         'st'        : 'st',
         'lyx'       : 'lyx',
         'r'         : 'Rscript',
         'sas'       : 'sas'},
    'nt': 
        {'stata'     : '%STATAEXE%',
         'matlab'    : 'matlab',
         'perl'      : 'perl',
         'python'    : 'python',
         'math'      : 'math',
         'st'        : 'st',
         'lyx'       : 'lyx',
         'r'         : 'Rscript',
         'sas'       : 'sas'}
}

extensions = {
    'stata'     : ['.do'],
    'matlab'    : ['.m'],
    'perl'      : ['.pl'],
    'python'    : ['.py'],
    'math'      : ['.m'],
    'st'        : ['.stc', '.stcmd'],
    'lyx'       : ['.lyx'],
    'r'         : ['.r', '.R'],
    'sas'       : ['.sas']
}