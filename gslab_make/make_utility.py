#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import yaml
import shutil
import traceback

from termcolor import colored
import colorama
colorama.init()

import gslab_make.private.messages as messages
import gslab_make.private.metadata as metadata
from gslab_make.private.exceptionclasses import CritError, ColoredError
from gslab_make.private.utility import get_path, format_message, norm_path


def check_os(osname = os.name):
    """Check OS is either POSIX or NT. 
    
    Parameters
    ----------
    osname : str, optional
        Name of OS. Defaults to ``os.name``.

    Returns
    -------
    None
    """

    if osname not in ['posix', 'nt']:
        raise CritError(messages.crit_error_unknown_system % osname)


def update_executables(paths, osname = os.name):
    """.. Update executable names using user configuration file. 
    
    Updates executable names with executables listed in user configuration file ``config_user``.
    
    Note
    ----
    Executable names are used by `program functions`_.
    
    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain values for all keys listed below.
    osname : str, optional
        Name of OS. Defaults to ``os.name``.

    Path Keys
    ---------
    config_user : str
        Path of user configuration file.   

    Returns
    -------
    None
    """

    try:
        config_user = get_path(paths, 'config_user')
        config_user = yaml.load(open(config_user, 'rb'))
    
        check_os(osname)
    
        if config_user['local']['executables']:
            metadata.default_executables[osname].update(config_user['local']['executables'])
    except:
        error_message = 'Error with update_executables. Traceback can be found below.' 
        error_message = format_message(error_message) 
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def update_mappings(paths, mapping_dict = {}):
    """.. Update path mappings using user configuration file. 
    
    Updates dictionary ``path_mappings`` with externals listed in user configuration file ``config_user``.
    
    Note
    ----
    Path mappings are used by `sourcing functions`_.
    
    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain values for all keys listed below.
    mapping_dict : dict, optional
        Dictionary of path mappings used to parse paths to update. 
        Defaults to no mappings.

    Path Keys
    ---------
    config_user : str
        Path of user config file.  

    Returns
    -------
    mapping_dict : dict
        Dictionary of path mappings used to parse paths. 
    """

    try:
        config_user = get_path(paths, 'config_user')
        config_user = yaml.load(open(config_user, 'rb'))

        if config_user['external']:
            mapping_dict.update(config_user['external'])

        return(mapping_dict)
    except:
        error_message = 'Error with update_mappings. Traceback can be found below.' 
        error_message = format_message(error_message) 
        raise_from(ColoredError(error_message, traceback.format_exc()), None)


def copy_output(file, copy_dir):
    """.. Copy output file.
    
    Copies output `file` to directory `copy_dir` with user prompt to confirm copy.
    
    Parameters
    ----------
    file : str
        Path of file to copy.
    copy_dir : str
        Directory to copy file.

    Returns
    -------
    None
    """

    file = norm_path(file)
    copy_dir = norm_path(copy_dir)
    message = colored(messages.warning_copy, color = 'cyan')
    
    try:
        upload = raw_input(message % (file, copy_dir))
    except:
        upload = input(message % (file, copy_dir))

    if upload.lower().strip() == "yes":
        shutil.copy(file, copy_dir)