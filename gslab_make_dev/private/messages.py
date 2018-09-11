#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)
        
######################################################
# Define Messages
######################################################      
    
# 1) Critical Errors
crit_error_no_makelog = 'ERROR! Makelog "%s" not found (either not started or deleted)'
crit_error_unknown_system = 'ERROR! Only the following operating systems are supported: "POSIX", "NT"'
crit_error_bad_command = 'ERROR! Command "%s" executed with errors'
crit_error_extension = 'ERROR! "%s" does not have the right program extension'
crit_error_no_file = 'ERROR! File "%s" not found'
crit_error_no_file_wildcard = 'ERROR! Files matching "%s" not found'
crit_error_bad_link = 'ERROR! Link "%s" incorrectly specified' 
crit_error_not_dir = 'ERROR! Path "%s" is not a directory' 
crit_error_log = 'ERROR! Cannot open log file "%s"'

# 2) Syntax Errors
syn_error_file_list = 'ERROR! Files must be specified in a list'
syn_error_wildcard = 'ERROR! Symlink and target must have same number of wildcards'
syn_error_options = 'ERROR! Duplicate options specified'

# 3) Notes & Warnings
note_makelog_start = 'Makelog started: '
note_makelog_end = 'Makelog ended: '
note_working_directory = 'Working directory: '
note_dash_separator = '-' * 80