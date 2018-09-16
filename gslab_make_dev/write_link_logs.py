#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import traceback

import gslab_make_dev.private.metadata as metadata
import gslab_make_dev.private.messages as messages
from gslab_make_dev.private.exceptionclasses import CritError
from gslab_make_dev.private.utility import glob_recursive, format_error
from gslab_make_dev.write_logs import write_to_makelog, write_stats_log, write_heads_log


def write_link_logs(link_map,
                    link_statslog = metadata.settings['link_statslog'],
                    link_headslog = metadata.settings['link_headslog'],
                    link_maplog = metadata.settings['link_maplog'],
                    recursive = float('inf'), 
                    makelog = metadata.settings['makelog']):        
    """ Write link logs.

    Notes
    -----
    The following information is logged:
        * Mapping of symlinks to targets (link map log)
        * Details on files contained in targets: 
            * File name (link statistics log)
            * Last modified (link statistics log)
            * File size (link statistics log)
            * File head (link headers log)
        * When walking through target directories, recursive determines depth.

    Parameters
    ----------
    link_map : list 
        Mapping of symlinks to targets (returned from `LinksList.create_symlinks`).
    link_statslog : str, optional
        Path to write link statistics log. Defaults to path specified in metadata.
    link_headslog : str, optional
        Path to write link headers log. Defaults to path specified in metadata.
    link_maplog : str, optional
        Path to write link map log. Defaults to path specified in metadata.
    recursive : int, optional
        Level of depth when walking through target directories. Defaults to infinite.
    makelog : str, optional
        Path of makelog. Defaults to path specified in metadata.

    Returns
    -------
    None
    """

    try:
        target_list = [target for target, symlink in link_map]
        target_list = [glob_recursive(target, recursive) for target in target_list]
        target_files = [f for target in target_list for f in target]

        write_stats_log(link_statslog, target_files)
        write_heads_log(link_headslog, target_files)    
        write_link_maplog(link_maplog, link_map)
        write_to_makelog('Link logs successfully written!', makelog)  
    except:
        error = 'ERROR! See `write_link_logs`:\n' + traceback.format_exc()
        error = format_error(error)
        write_to_makelog(error, makelog)
        raise CritError(error)

def write_link_maplog(link_maplog, link_map):
    """ Make link map log.

    Parameters
    ----------
    link_maplog : str
        Path to write link map log.
    link_map : list 
        Mapping of symlinks to targets (returned by LinksList).

    Returns
    -------
    None
    """
    
    header = 'target\tsymlink'

    with open(link_maplog, 'w') as MAPLOG:
        print(header, file = MAPLOG)

        for target, symlink in link_map:
            print("%s\t%s" % (target, symlink), file = MAPLOG)
        
      
