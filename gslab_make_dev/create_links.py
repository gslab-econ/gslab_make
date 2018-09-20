#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import traceback

import gslab_make_dev.private.metadata as metadata
from gslab_make_dev.private.exceptionclasses import CritError
from gslab_make_dev.private.linkdirective import LinksList
from gslab_make_dev.private.utility import format_error
from gslab_make_dev.write_logs import write_to_makelog


def create_links(file_list,
                 link_dir = metadata.settings['link_dir'],
                 makelog = metadata.settings['makelog']):
    """ Create symlinks from list of files containing linking instructions.

    Parameters
    ----------
    file_list : list
        List of files containing linking instructions.
    link_dir : str, optional
        Directory to write symlinks. Defaults to directory specified in metadata.
    makelog : str, optional
        Path of makelog. Defaults to path specified in metadata.

    Returns
    -------
    link_map : list
        List of (target, symlink) for each symlink created.
    """

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