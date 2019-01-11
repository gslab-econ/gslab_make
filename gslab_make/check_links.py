#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import git

import gslab_make.private.messages as messages
from gslab_make.private.utility import norm_path, format_error, glob_recursive
from gslab_make.write_logs import write_to_makelog


def get_git_status(repo): 
    root = repo.working_tree_dir

    file_list = repo.git.status(porcelain = True)
    file_list = file_list.split('\n')
    file_list = [f.lstrip().lstrip('MADRCU?!').lstrip() for f in file_list]
    file_list = [root + "/" + f for f in file_list]
    file_list = [norm_path(f) for f in file_list]

    return(file_list)

def get_modified_links(paths, 
                       link_map, 
                       recursive = float('inf')):

    target_list = [target for target, symlink in link_map]
    target_list = [glob_recursive(target, recursive) for target in target_list]
    target_files = [f for target in target_list for f in target]
    target_files = set(target_files)
   
    repo = git.Repo('.', search_parent_directories = True)    
    modified = get_git_status(repo)
    overlap = [l for l in target_files if l in modified]
    
    if overlap:
        message = format_error(messages.note_modified_files % '\n'.join(overlap))
        write_to_makelog(paths, message)
        print(message)

