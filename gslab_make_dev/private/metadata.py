#! /usr/bin/env python

######################################################
# Define Metadata
######################################################	

makelog_started = False

# Commands
commands = {
    'posix': 
        {'makelink'  : 'ln -s \"%s\" \"%s\"', 
         'rmdir'     : 'rmdir %s \"%s\"', 
         'stata'     : '%s %s do %s',
         'matlab'    : '%s %s -r run(\'%s\') -logfile %s',
         'perl'      : '%s %s %s %s',
         'python'    : '%s %s %s %s',
         'math'      : '%s < %s %s',
         'st'        : '%s %s',
         'lyx'       : '%s %s %s',
         'r'         : '%s %s %s',
         'sas'       : '%s %s -log -print %s'},
    'nt': 
        {'makelink'  : 'mklink %s \"%s\" \"%s\"', 
         'rmdir'     : 'rm %s \"%s\"', 
         'stata'     : '%s %s do %s',
         'matlab'    : '%s %s -r run(\'%s\') -logfile %s',
         'perl'      : '%s %s %s %s',
         'python'    : '%s %s %s %s',
         'math'      : '%s < %s %s',
         'st'        : '%s %s',
         'lyx'       : '%s %s %s',
         'r'         : '%s %s %s',
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
        {'stata'     : 'statamp',
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
    'stata'     : '.do',
    'matlab'    : '.m',
    'perl'      : '.pl',
    'python'    : '.py',
    'math'      : '.m',
    'st'        : ['.stc', '.stcmd'],
    'lyx'       : '.lyx',
    'r'         : '.R',
    'rinstall'  : '',
    'sas'       : '.sas',
    'other'     : ''
}

# Settings
settings = {
    'link_dir'        : '../input/',
    'temp_dir'        : '../temp/',
    'output_dir'      : '../output/',
    'makelog'         : '../log/make.log',
    'output_statslog' : '../log/output_stats.log',
    'output_headslog' : '../log/output_heads.log', 
    'link_maplog'     : '../log/link_map.log',
    'link_statslog'   : '../log/link_stats.log',
    'link_headslog'   : '../log/link_heads.log'
}
