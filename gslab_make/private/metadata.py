# -*- coding: utf-8 -*-
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

# ~~~~~~~~~~~~~~~ #
# Define metadata #
# ~~~~~~~~~~~~~~~ #

makelog_started = False

color_success = None
color_failure = 'red'
color_in_process = 'cyan'

commands = {
    'posix': 
        {'makecopy' : 'cp -a \"%s\" \"%s\"', 
         'makelink' : 'ln -s \"%s\" \"%s\"',          
         'rmdir'    : 'rm %s \"%s\"', 
         'jupyter'  : '%s nbconvert --ExecutePreprocessor.timeout=-1 %s \"%s\"',
         'lyx'      : '%s %s \"%s\"',
         'latex'    : '%s -output-directory=%slatex_auxiliary_dir %s \"%s\"',
         'math'     : '%s < \"%s\" %s',
         'matlab'   : '%s %s -r \"try run(\'%s\'); catch e, fprintf(getReport(e)), exit(1); end; exit(0)\" -logfile \"%s\"',
         'perl'     : '%s %s \"%s\" %s',
         'python'   : '%s %s \"%s\" %s',
         'julia'    : '%s %s \"%s\"',
         'r'        : '%s %s \"%s\"',
         'sas'      : '%s %s -log -print %s',
         'st'       : '%s \"%s\"',
         'stata'    : '%s %s do \\\"%s\\\"'},
    'nt': 
        {'makecopy' : '%s xcopy /E /Y /Q /I /K \"%s\" \"%s\"',
         'makelink' : 'mklink %s \"%s\" \"%s\"',        
         'rmdir'    : 'rmdir %s \"%s\"', 
         'jupyter'  : '%s nbconvert --ExecutePreprocessor.timeout=-1 %s \"%s\"',
         'lyx'      : '%s %s \"%s\"',
         'latex'    : '%s -output-directory=%slatex_auxiliary_dir %s \"%s\"',
         'math'     : '%s < \"%s\" %s',
         'matlab'   : '%s %s -r \"try run(\'%s\'); catch e, fprintf(getReport(e)), exit(1); end; exit(0)\" -logfile \"%s\"',
         'perl'     : '%s %s \"%s\" %s',
         'python'   : '%s %s \"%s\" %s',
         'julia'    : '%s %s \"%s\"',
         'r'        : '%s %s \"%s\"',
         'sas'      : '%s %s -log -print %s',
         'st'       : '%s \"%s\"',
         'stata'    : '%s %s do \\\"%s\\\"'},
}

default_options = {
    'posix': 
        {'rmdir'    : '-rf', 
         'jupyter'  : '--to notebook --inplace --execute',
         'lyx'      : '-e pdf2',
         'latex'    : '',
         'math'     : '-noprompt',
         'matlab'   : '-nosplash -nodesktop',
         'perl'     : '',
         'python'   : '',
         'julia'    : '',
         'r'        : '--no-save',
         'sas'      : '',
         'st'       : '',
         'stata'    : '-e'},
    'nt': 
        {'rmdir'    : '/s /q', 
         'jupyter'  : '--to notebook --inplace --execute',
         'lyx'      : '-e pdf2',
         'latex'    : '',
         'math'     : '-noprompt',
         'matlab'   : '-nosplash -minimize -wait',
         'perl'     : '',
         'python'   : '',
         'r'        : '--no-save',
         'sas'      : '-nosplash',
         'st'       : '',
         'stata'    : '/e'}
}

default_executables = {
    'posix': 
        {'git-lfs'  : 'git-lfs', 
         'jupyter'  : 'python -m jupyter',
         'lyx'      : 'lyx',
         'latex'    : 'pdflatex',
         'math'     : 'math',
         'matlab'   : 'matlab',
         'perl'     : 'perl',
         'python'   : 'python',
         'r'        : 'Rscript',
         'sas'      : 'sas',
         'st'       : 'st',
         'stata'    : 'stata-mp',
         'julia'    : 'julia'},
    'nt': 
        {'git-lfs'  : 'git-lfs',
         'jupyter'  : 'python -m jupyter',
         'lyx'      : 'LyX2.3',
         'latex'    : 'pdflatex',
         'math'     : 'math',
         'matlab'   : 'matlab',
         'perl'     : 'perl',
         'python'   : 'python',
         'r'        : 'Rscript',
         'sas'      : 'sas',
         'st'       : 'st',
         'stata'    : 'StataMP-64',
         'julia'    : 'julia'},
}

extensions = {
    'jupyter' : ['.ipynb', '.IPYNB'],
    'lyx'     : ['.lyx', '.LYX'],
    'latex'   : ['.tex', '.TEX'],
    'math'    : ['.m', '.M'],
    'matlab'  : ['.m', '.M'],
    'perl'    : ['.pl', '.PL'],
    'python'  : ['.py', '.PY'],
    'r'       : ['.r', '.R'],
    'sas'     : ['.sas', '.SAS'],
    'st'      : ['.stc', '.STC', '.stcmd', '.STCMD'],
    'stata'   : ['.do', '.DO'],
    'julia'   : ['.jl', '.JL']
}