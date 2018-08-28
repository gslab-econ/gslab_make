#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os

from gslab_make_dev.dir_mod import remove_path
from gslab_make_dev.private.linkdirective import LinksList
from gslab_make_dev.private.utility import start_log, end_log
import gslab_make_dev.private.metadata as metadata


def make_links(file_list,
               link_dir = metadata.settings['link_dir'],
               makelog = metadata.settings['makelog']):

    LINKLOG = start_log(metadata.settings['linklog'], 'Linklog')
        
    link_list = LinksList(file_list, link_dir)
    link_list = link_list.make_symlinks()
        
    end_log(LINKLOG, 'Linklog', makelog)
        
    return(link_list)

    # try:         
    #     LINKLOG = start_log(metadata.settings['linklog'], 'Linklog')
        
    #     link_list = LinksList(file_list, link_dir)
    #     link_list = link_list.make_symlinks()
        
    #     end_log(LINKLOG, 'Linklog', makelog)
        
    #     return(link_list)
        
    # except Exception as error:
    #     print("Error with make_links: \n", error)
    #     raise Exception                    
