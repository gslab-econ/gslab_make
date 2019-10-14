#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import traceback

from termcolor import colored
import colorama
colorama.init()

import gslab_make.private.metadata as metadata
from gslab_make.private.exceptionclasses import ColoredError
from gslab_make.private.utility import norm_path, get_path, glob_recursive, format_message
from gslab_make.write_logs import write_to_makelog, _write_stats_log, _write_heads_log


def write_source_logs(paths, 
                      source_map,
                      depth = float('inf')):        
    """Write source logs.

    Notes
    -----
    The following information is logged:
    * Mapping of symlinks/copies to sources (source map log)
    * Details on files contained in sources: 
    * File name (source statistics log)
    * Last modified (source statistics log)
    * File size (source statistics log)
    * File head (source headers log)
    * When walking through source directories, depth determines depth.

    Parameters
    ----------
    paths : :obj:`dict` 
        Dictionary of paths. Dictionary should contain values for all keys listed below.
    source_map : :obj:`list `
        Mapping of symlinks/copies (destination) to sources (returned from :mod:`MoveList.create_symlinks` or :mod:`MoveList.create_copies`).
    depth : :obj:`float`, optional
        Level of depth when walking through source directories. Defaults to infinite.

    Path Keys
    ---------
    source_statslog : :obj:`str`
       Path to write source statistics log.
    source_headslog : :obj:`str`
       Path to write source headers log.
    source_maplog : :obj:`str`
       Path to write source map log.
    makelog : :obj:`str`
       Path of makelog.

    Returns
    -------
    None
    """

    try:
        source_statslog = get_path(paths, 'source_statslog')
        source_headslog = get_path(paths, 'source_headslog')
        source_maplog   = get_path(paths, 'source_maplog')

        source_list = [source for source, destination in source_map]
        source_list = [glob_recursive(source, depth) for source in source_list]
        source_files = [f for source in source_list for f in source]
        source_files = set(source_files)

        """IF WE DECIDE TO ALLOW FOR RAW SUBDIRECTORIES WITHOUT LINKING
        raw_dir = get_path(paths, 'raw_dir')
        raw_files = glob_recursive(raw_dir)
        source_files = set(source_files + raw_files)
        """

        if source_statslog:
            source_statslog = norm_path(source_statslog)
            write_stats_log(source_statslog, source_files)

        if source_headslog:
            source_headslog = norm_path(source_headslog)
            write_heads_log(source_headslog, source_files)   

        if source_maplog:
            source_maplog = norm_path(source_maplog)
            _write_source_maplog(source_maplog, source_map)

        message = 'Source logs successfully written!'
        write_to_makelog(paths, message)  
        print(colored(message, metadata.color_success))
    except:
        error_message = 'Error with `write_source_logs`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def _write_source_maplog(source_maplog, source_map):
    """Write link map log.

    Parameters
    ----------
    source_maplog : :obj:`str`
        Path to write link map log.
    source_map : :obj:`list` 
        Mapping of symlinks to sources (returned by :mod:`LinksList`).

    Returns
    -------
    None
    """
    
    header = 'destination | source'

    with open(source_maplog, 'w') as MAPLOG:
        print(header, file = MAPLOG)

        for source, destination in source_map:
            destination = os.path.relpath(destination)
            print("%s | %s" % (destination, source), file = MAPLOG)