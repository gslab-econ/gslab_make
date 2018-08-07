#! /usr/bin/env python

######################################################
# Define Metadata
######################################################	

makelog_started = False

# Commands
commands = {
    'makelinkwin'   : 'mklink %s \"%s%s\" \"%s%s\"',
    'makelinkunix'  : 'ln -s \"%s%s\" \"%s%s\"',
    'rmdirwin'      : 'rmdir %s \"%s\"',
    'rmdirunix'     : 'rm %s \"%s\"',
    'stata'         : '%s %s do %s',
    'matlab'        : '%s -r %s -logfile %s %s',
    'perl'          : '%s %s %s %s',
    'python'        : '%s %s %s %s',
    'math'          : '%s < %s %s',
    'st'            : '%s %s',
    'lyx'           : '%s %s %s',
    'rbatch'        : '%s %s %s %s',
    'rinstall'      : '%s %s %s %s',
    'sas'           : '%s %s %s'
}

default_options = {
    'rmdirwin'   : '/s /q',
    'rmdirunix'  : '-rf',
    'matlabwin'  : '-nosplash -minimize -wait',
    'matlabunix' : '-nosplash -nodesktop',
    'statawin'   : '/e',
    'stataunix'  : '-e',
    'rbatch'     : '--no-save',
    'rinstall'   : '--no-multiarch',
    'saswin'     : '-nosplash',
    'math'       : '-noprompt',
    'lyx'        : '-e pdf2'
}

option_overlaps = {
    'matlab'    : {'log': '-logfile'},
    'sas'       : {'log': '-log', 'lst': '-print'}
}

default_executables = {
    'statawin'      : '%STATAEXE%',
    'stataunix'     : 'statamp',
    'matlab'        : 'matlab',
    'perl'          : 'perl',
    'python'        : 'python',
    'math'          : 'math',
    'st'            : 'st',
    'lyx'           : 'lyx',
    'rbatch'        : 'R CMD BATCH',
    'rinstall'      : 'R CMD INSTALL',
    'sas'           : 'sas'
}

extensions = {
    'stata'         : '.do',
    'matlab'        : '.m',
    'perl'          : '.pl',
    'python'        : '.py',
    'math'          : '.m',
    'stc'           : '.stc',
    'stcmd'         : '.stcmd',
    'lyx'           : '.lyx',
    'rbatch'        : '.R',
    'rinstall'      : '',
    'sas'           : '.sas',
    'other'         : ''
}

option_start_chars = ['-', '+']

# Locals
file_loc = {
    'gslab_l' : r'//Gentzkow-dt1/GSLAB_L'
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
