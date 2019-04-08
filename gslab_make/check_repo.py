#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import git
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     

def convert_size_to_bytes(size_str):
    multipliers = {
        ' B': 1024 ** 0,
        'KB': 1024 ** 1,
        'MB': 1024 ** 2,
        'GB': 1024 ** 3,
        'TB': 1024 ** 4,
        'PB': 1024 ** 5,
    }

    for suffix in multipliers:
        if size_str.endswith(suffix):
            size = float(size_str[0:-len(suffix)]) * multipliers[suffix]
            return size
            
def parse_git_ls(text):
    text = text.split()
    
    file = text[4]
    size = text[3]
    size = float(size)
    
    return (file, size)
    
def parse_lfs_ls(text):
    text = text.split(' ', 2)[2].rsplit('(', 1)
    
    file = text[0].strip()
    size = text[-1].strip(')')
    size = convert_size_to_bytes(size)
    
    return (file, size)
   
def check_repository_size(paths):
    """ Check repository size

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'config' : str
                Path of config YAML file.
        }

    Returns
    -------
    None
    """
    
    repo = git.Repo('.', search_parent_directories = True)    
    g = git.Git(repo)
    
    files = g.execute('git ls-tree -r -l HEAD').split('\n')
    files = [parse_git_ls(f) for f in files]
    files = {file: size for (file, size) in files}
            
    lfs_files = g.execute('git lfs ls-files --size').split('\n')   
    lfs_files = [parse_lfs_ls(f) for f in lfs_files]
    lfs_files = {file: size for (file, size) in lfs_files}
    
    for key in lfs_files.keys():
        files.pop(key, None)
    
    files = sum(files.values())
    lfs_files = sum(lfs_files.values())
    max_file_sizes:
        
    file_MB_limit_lfs: 2               # Soft limit on file size (w/ LFS)
    total_MB_limit_lfs: 500            # Soft limit on total size (w/ LFS)  
    file_MB_limit: 0.5                 # Soft limit on file size (w/o LFS)
    total_MB_limit: 125                # Soft limit on total size (w/o LFS)
  