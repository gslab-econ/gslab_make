#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import traceback

from gslab_make.private.linkdirective import LinksList
from gslab_make.private.utility import format_error
from gslab_make.write_logs import write_to_makelog


def create_links(paths,
                 file_list,, 
                 mapping_dict = {}):
    """ Create symlinks from list of files containing linking instructions.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'move_dir' : str
                Directory to write symlinks.
            'makelog' : str
                Path of makelog.
        }
    file_list : list
        List of files containing linking instructions.
    mapping_dict : dict, optional
        Dictionary of path mappings used to parse linking instructions. 
        Defaults to no mappings.

    Returns
    -------
    move_map : list
        List of (source, destination) for each symlink created.
    """

    move_dir = paths['move_dir']

    try:              
        move_list = MoveList(file_list, file_format, move_dir, mapping_dict)
        if move_list.move_directive_list:
            os.makedirs(move_dir)
            move_map = move_list.create_symlinks()       
        else:
            move_map = []

        write_to_makelog(paths, 'Links successfully created!')    
        return(move_map)
    except:
        error_message = 'An error was encountered with `create_links`. Traceback can be found below.' 
        error_message = format_error(error_message) + '\n' + traceback.format_exc()
        write_to_makelog(paths, error_message)
        
        raise               


def copy_inputs(paths,
                file_list,
                mapping_dict = {}):
    """ Create copies to inputs from list of files containing copying instructions.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'input_dir' : str
                Directory to write copies.
            'makelog' : str
                Path of makelog.
        }
    file_list : list
        List of files containing copying instructions.
    mapping_dict : dict, optional
        Dictionary of path mappings used to parse copying instructions. 
        Defaults to no mappings.

    Returns
    -------
    move_map : list
        List of (source, destination) for each copy created.
    """

    link_dir = paths['input_dir']

    try:              
        link_list = LinksList(file_list, "input", link_dir, mapping_dict, True)
        if link_list.link_directive_list:
            os.makedirs(link_dir)
            link_map = link_list.create_symlinks()       
        else:
            link_map = []

        write_to_makelog(paths, 'Copies successfully created!')    
        return(link_map)
    except:
        error_message = 'An error was encountered with `copy_inputs`. Traceback can be found below.' 
        error_message = format_error(error_message) + '\n' + traceback.format_exc()
        write_to_makelog(paths, error_message)
        
        raise    


def link_inputs(paths,
                file_list,
                mapping_dict = {}):
    """ 
    Create symlinks to inputs from list of files containing linking instructions. 

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'input_dir' : str
                Directory to write symlinks.
            'makelog' : str
                Path of makelog.
        }
    file_list : list
        List of files containing linking instructions.
    mapping_dict : dict, optional
        Dictionary of path mappings used to parse linking instructions. 
        Defaults to no mappings.

    Returns
    -------
    move_map : list
        List of (source, destination) for each symlink created.
    """
    paths['move_dir'] = paths['input_dir']
    move_map = create_links(paths, file_list, mapping_dict)
    return(move_map)


def link_externals(paths,
                   file_list,
                   mapping_dict = {}):
    """ 
    Create symlinks to externals from list of files containing linking instructions. 

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'external_dir' : str
                Directory to write symlinks.
            'makelog' : str
                Path of makelog.
        }
    file_list : list
        List of files containing linking instructions.
    mapping_dict : dict, optional
        Dictionary of path mappings used to parse linking instructions. 
        Defaults to no mappings.

    Returns
    -------
    move_map : list
        List of (source, destination) for each symlink created.
    """
    paths['move_dir'] = paths['external_dir']
    move_map = create_links(paths, file_list, mapping_dict)
    return(move_map)