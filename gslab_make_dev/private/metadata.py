#! /usr/bin/env python

######################################################
# Define Metadata
######################################################	

makelog_started = False

# Commands
commands = {
    'posix': 
        {'makelink'  : 'mklink %s \"%s%s\" \"%s%s\"', 
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
        {'makelink'  : 'ln -s \"%s%s\" \"%s%s\"', 
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

# Settings (directory keys must end in 'dir' and file keys must end in 'file')
settings = {
    'links_dir'         : '../external_links/',
    'linkslog_file'     : './make_links.log',
    'output_dir'        : '../output/',
    'output_local_dir'  : '../output_local/',
    'temp_dir'          : '../temp/',
    'makelog_file'      : '../output/make.log',
    'manifest_file'     : '../output/data_file_manifest.log',
    'link_logs_dir'     : '../log/',
    'link_stats_file'   : 'link_stats.log',
    'link_heads_file'   : 'link_heads.log',
    'link_orig_file'    : 'link_orig.log',
    'stats_file'        : 'stats.log',
    'heads_file'        : 'heads.log'
}
