#! /usr/bin/env python
from __future__ import absolute_import, division, print_function
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import private.metadata as metadata

from make_logs import write_stats_log, write_heads_log
from private.utility import glob_recursive


def make_link_logs(link_map,
                   link_statslog = metadata.settings['link_statslog'],
                   link_headslog = metadata.settings['link_headslog'],
                   link_maplog = metadata.settings['link_maplog'],
                   recursive = float('inf')):     
    
    target_list = [target for target, symlink in link_map]
    target_list = [glob_recursive(target, recursive) for target in target_list]
    target_files = [f for target in target_list for f in target]

    write_stats_log(link_statslog, target_files)
    write_heads_log(link_headslog, target_files)    
    make_link_maplog(link_maplog, link_map)
    

def make_link_maplog(link_maplog, link_map):

    header = 'target\tsymlink'

    with open(link_maplog, 'w') as MAPLOG:
        print(header, file = MAPLOG)

        for target, symlink in link_map:
            print("%s\t%s" % (target, symlink), file = MAPLOG)
        
      
