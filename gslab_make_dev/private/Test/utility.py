#! /usr/bin/env python

def invert_dict(d):
    d = {v: k for k, v in d.iteritems()}
    return(d)