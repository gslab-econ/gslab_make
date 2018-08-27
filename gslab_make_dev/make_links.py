#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os

from dir_mod import remove_path
from private.linkdirective import LinksList
from private.utility import start_log, end_log
import private.metadata as metadata


def make_links(file_list,
               link_dir = metadata.settings['link_dir'],
               makelog = metadata.settings['makelog']):

    try:         
        LINKLOG = start_log(metadata.settings['linkslog_file'], 'Linklog')

        if os.path.exists(list.link_dir):
            remove_path(list.link_dir)
            os.makedirs(list.link_dir)  
        
        link_list = LinksList(file_list, link_dir)
        link_list = link_list.make_symlinks()
        
        end_log(LINKLOG, makelog, 'Linklog')
        
        return(link_list)
        
    except Exception as error:
        print("Error with make_links: \n", error)
        raise Exception                    
