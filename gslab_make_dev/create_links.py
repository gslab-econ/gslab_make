#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import traceback

import gslab_make_dev.private.messages as messages
from gslab_make_dev.private.linkdirective import LinksList
from gslab_make_dev.private.utility import format_error
from gslab_make_dev.write_logs import write_to_makelog


def create_links(paths,
                 file_list):
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
    makelog  = paths['makelog']   

    try:              
        link_list = LinksList(file_list, link_dir)
        link_map = link_list.create_symlinks()       
        write_to_makelog('Links successfully created!', makelog)    
        
        return(link_map)
    except:
        error_message = 'An error was encountered with `create_links`' 
        error_message = format_error(error_message) + '\n' + traceback.format_exc()
        write_to_makelog(error_message, makelog)
        
        raise               
