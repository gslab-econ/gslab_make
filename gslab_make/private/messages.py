#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)
        
######################################################
# Define Messages
######################################################      
    
# 1) Critical Errors
(X) crit_error_unknown_system = 'ERROR! Only the following operating systems are supported: `POSIX`, `NT`.' 
(X) crit_error_no_makelog = 'ERROR! Makelog `%s` not found. Makelog either not started (via `start_makelog`) or deleted after started.' 
(X) crit_error_no_program_output = 'ERROR! Certain applications (`matlab`, `sas`, and `stata`) automatically create program outputs when ran using system command. Program output `%s` from `%s` cannot be not found.' # FILL IN
(X) crit_error_no_file = 'ERROR! File `%s` not found.' 
crit_error_no_files = 'ERROR! Files `%s` not found.'
crit_error_no_path = 'ERROR! Path `%s` not found.' 
crit_error_no_path_wildcard = 'ERROR! Paths matching `%s` not found.' 
(X) crit_error_bad_command = 'ERROR! Command `%s` cannot be executed by operating system. Command may be misspecified or does not exist. Traceback can be found below:' 
crit_error_bad_link = 'ERROR! Link `%s` incorrectly specified (check if correctly delimited).' 
(X) crit_error_extension = 'ERROR! Program `%s` does not have correct extension. Program should have one of the following extensions: %s' 
crit_error_path_mapping = 'ERROR! `{%s}` found in linking instructions but not in path mapping.'
crit_error_no_repo = 'ERROR! Current working directory is not part of a git repository.'

# 2) Syntax Errors
syn_error_wildcard = 'ERROR! Symlink and target must have same number of wildcards.' 
syn_error_options = 'ERROR! Duplicate options specified.' 

# 3) Type errors
type_error_file_list = 'ERROR! Files must be specified in a list.' 
type_error_not_dir = 'ERROR! Path `%s` is not a directory.' 

# 4) Warnings
(X) warning_glob = 'WARNING! No files were returned by `glob_recursive` for path `%s` when walking to a depth of `%s`.'
warning_modified_files = "WARNING! The following target files have been modified according to git status:\n%s"
(X) warning_lyx_type = 'WARNING! Document type `%s` unrecognized. Reverting to default of no special document type.'

# 5) Notes
note_makelog_start = 'Makelog started: '
note_makelog_end = 'Makelog ended: '
note_working_directory = 'Working directory: '

note_dash_line = '-' * 80
note_star_line = '*' * 80 