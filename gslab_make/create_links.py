#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import traceback

import gslab_make.private.messages as messages
from gslab_make.private.linkdirective import LinksList
from gslab_make.private.utility import format_error
from gslab_make.write_logs import write_to_makelog


def create_links(paths,
                 file_list, 
                 path_dict):
    """ Create symlinks from list of files containing linking instructions.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'link_dir' : str
                Directory to write symlinks.
            'makelog' : str
                Path of makelog.
        }
    file_list : list
        List of files containing linking instructions.

    Returns
    -------
    link_map : list
        List of (target, symlink) for each symlink created.
    """

    link_dir = paths['link_dir']

    try:              
        link_list = LinksList(file_list, link_dir, path_dict)
        if link_list.link_directive_list:
            os.makedirs(link_dir)
            link_map = link_list.create_symlinks()       
        else:
            link_map = []

        write_to_makelog(paths, 'Links successfully created!')    
        return(link_map)
    except:
        error_message = 'An error was encountered with `create_links`' 
        error_message = format_error(error_message) + '\n' + traceback.format_exc()
        write_to_makelog(paths, error_message)
        
        raise               