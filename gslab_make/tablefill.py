#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import re
import traceback
from itertools import chain

from termcolor import colored
import colorama
colorama.init()

import gslab_make.private.messages as messages
from gslab_make.private.exceptionclasses import CritError, ColoredError
from gslab_make.private.utility import norm_path, format_message
from gslab_make.write_logs import write_to_makelogs

def parse_tag(tag):
    """ Parse tag from input."""
    
    if not re.match('<Tab:(.*)>\n', tag, flags = re.IGNORECASE):
        raise Exception
    else:
        tag = re.sub('<Tab:(.*?)>\n', r'\g<1>', tag, flags = re.IGNORECASE)
        tag = tag.lower()
        
    return(tag)
    
    
def parse_data(data, null):
    """ Parse data from input.
    
    Parameters
    ----------
    data : list
        Input data to parse.
    null : str
        String to replace null characters.

    Returns
    -------
    data : list
        List of data values from input.
    """
    null_strings = ['', '.', 'NA']
    
    data = [row.strip().split('\t') for row in data]
    data = chain(*data)
    data = [value.strip() for value in data]
    if (null != None):
        data = [null if value in null_strings else value for value in data]
    
    return(data)
        
    
def parse_content(file, null):
    """ Parse content from input."""
        
    with open(file, 'r') as f:
        content = f.readlines()
        
    try:
        tag = parse_tag(content[0])
    except:
        raise_from(CritError(messages.crit_error_no_tag % file), None)   
    
    data = parse_data(content[1:], null)
    
    return(tag, data)
    
    
def insert_value(line, value, type):
    if (type == 'no change'):
        line = line.replace('###', value)
    elif (type == 'round'):
        try:
            value = float(value)
        except:
            raise_from(CritError(messages.crit_error_not_float % value), None)

        digits = re.findall('#([0-9]+)#', line)[0]
        rounded_value = format(value, '.%sf' % digits)
        line = re.sub('(.*)#[0-9]+#', r'\g<1>' + rounded_value, line)
    elif (type == 'comma + round'):
        try:
            value = float(value)
        except:
            raise_from(CritError(messages.crit_error_not_float % value), None)

        digits = re.findall('#([0-9]+),#', line)[0]
        rounded_value = format(value, ',.%sf' % digits)
        line = re.sub('(.*)#[0-9]+,#', r'\g<1>' + rounded_value, line)

    return(line)


def insert_tables_lyx(template, tables):
    with open(template, 'r') as f:
        doc = f.readlines()
      
    is_table = False

    for i in range(len(doc)):
        if doc[i].startswith('name "tab:'):
            tag = doc[i].replace('name "tab:','').rstrip('"\n').lower()
            
            try:
                values = tables[tag]
                entry_count = 0
                is_table = True
            except KeyError:
                pass

        while is_table:
            try:
                if re.match('.*###', doc[i]):
                    doc[i] = insert_value(doc[i], values[entry_count], 'no change')
                    entry_count += 1
                    break
                elif re.match('.*#[0-9]+#', doc[i]):
                    doc[i] = insert_value(doc[i], values[entry_count], 'round')
                    entry_count += 1
                    break
                elif re.match('.*#[0-9]+,#', doc[i]):
                    doc[i] = insert_value(doc[i], values[entry_count], 'comma + round')
                    entry_count += 1
                    break
                elif re.match('</lyxtabular>', doc[i]):
                    is_table = False
                    if entry_count != len(values):
                        raise_from(CritError(messages.crit_error_too_many_values % tag), None)
                else:
                    break
            except KeyError:
                raise_from(CritError(messages.crit_error_not_enough_values % tag), None)
                

    doc = '\n'.join(doc)
    return(doc)


def insert_tables_latex(template, tables):
    with open(template, 'r') as f:
        doc = f.readlines()

    is_table = False

    for i in range(len(doc)):
        if doc[i].startswith('label{tab:'):
            tag = doc[i].split(':')[1].rstrip('}\n').strip('"').lower()
            
            try:
                values = tables[tag]
                entry_count = 0
                is_table = True
            except KeyError:
                pass

        while is_table:
            line_col = doc[i].split("&")

            for col in line_col:
                try:
                    if re.match('.*###', col):
                        col = insert_value(col, values[entry_count], 'no change')
                        entry_count += 1
                        break
                    elif re.match('.*#[0-9]+#', col):
                        col = insert_value(col, values[entry_count], 'round')
                        entry_count += 1
                        break
                    elif re.match('.*#[0-9]+,#', col):
                        col = insert_value(col, values[entry_count], 'comma + round')
                        entry_count += 1
                        break
                except KeyError:
                    raise_from(CritError(messages.crit_error_not_enough_values % tag), None)
                
            doc[i] = "&".join(line_col)
                
            if doc[i] == 'end{tabular}':
                is_table = False
                if entry_count != len(values):
                    raise_from(CritError(messages.crit_error_too_many_values % tag), None)
            else:
            	break


def insert_tables(template, tables):
    if re.search('\.lyx', template):
        doc = insert_tables_lyx(template, tables)
    elif re.search('\.tex', template):
        doc = insert_tables_latex(template, tables)

    return(doc)


def tablefill(inputs, template, output, null = None):
    try:
        inputs = [norm_path(file) for file in inputs]
        content = [parse_content(file, null) for file in inputs]
        tables = {tag:data for (tag, data) in content}
        
        if (len(content) != len(tables)):
            raise_from(CritError(messages.crit_error_duplicate_tables), None)

        doc = insert_tables(template, tables) 
        
        with open(output, 'w') as f:
            f.write(doc)
    except:
        error_message = 'Error with `tablefill`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise_from(ColoredError(error_message, traceback.format_exc()), None)