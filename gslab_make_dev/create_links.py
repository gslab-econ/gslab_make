#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

from write_logs import start_log, end_log
from private.linkdirective import LinksList
import private.metadata as metadata


def create_links(file_list,
                 link_dir = metadata.settings['link_dir']):
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
               
        return(link_map)
        
    except Exception as error:
        print("Error with make_links: \n", error)
        raise Exception                    
