#! /usr/bin/env python

import os

from dir_mod import remove_dir
from private.linkdirective import LinksList
from private.preliminaries import start_logging, end_logging
import private.metadata as metadata

def make_links(file_list,
               link_dir = metadata.settings['link_dir'],
               makelog = metadata.settings['makelog_file']):

    try:         
        LOGFILE = start_logging(metadata.settings['linkslog_file'], 'make_links.py')

        if os.path.exists(list.link_dir):
            remove_dir(list.link_dir)
            os.makedirs(list.link_dir)  
        
        link_list = LinksList(file_list, link_dir)
        link_list = link_list.make_symlinks()
        
        end_logging(LOGFILE, makelog, 'make_links.py')
        
        return(link_list)
        
    except Exception as error:
        print("Error with make_links: \n", error)
        raise Exception                    
