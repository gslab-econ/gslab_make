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

def _parse_tag(tag):
    """.. Parse tag from input."""
    
    if not re.match('<Tab:(.*)>\n', tag, flags = re.IGNORECASE):
        raise Exception
    else:
        tag = re.sub('<Tab:(.*?)>\n', r'\g<1>', tag, flags = re.IGNORECASE)
        tag = tag.lower()
        
    return(tag)
    
    
def _parse_data(data, null):
    """.. Parse data from input.
    
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
     
    data = [row.rstrip('\r\n') for row in data]
    data = [row for row in data if row]
    data = [row.split('\t') for row in data]
    data = chain(*data)
    data = [*data]
    if (null != None):
        data = [null if value in null_strings else value for value in data]
    
    return(data)
        
    
def _parse_content(file, null):
    """Parse content from input."""
        
    with open(file, 'r') as f:
        content = f.readlines()
        
    try:
        tag = _parse_tag(content[0])
    except:
        raise_from(CritError(messages.crit_error_no_tag % file), None)   
    
    data = _parse_data(content[1:], null)
    
    return(tag, data)
    
    
def _insert_value(line, value, type):
    """Insert value into line.
    
    Parameters
    ----------
    line : str
        Line of document to insert value.
    value : str
        Value to insert.
    type : str
        Formatting for value.

    Returns
    -------
    line : str
        Line of document with inserted value.
    """
    
    if (type == 'no change'):
        line = re.replace('\\\\?#\\\\?#\\\\?#', value, line)
    elif (type == 'round'):
        try:
            value = float(value)
        except:
            raise_from(CritError(messages.crit_error_not_float % value), None)

        digits = re.findall('\\\\?#([0-9]+)\\\\?#', line)[0]
        rounded_value = format(value, '.%sf' % digits)
        line = re.sub('(.*?)\\\\?#[0-9]+\\\\?#', r'\g<1>' + rounded_value, line)
    elif (type == 'comma + round'):
        try:
            value = float(value)
        except:
            raise_from(CritError(messages.crit_error_not_float % value), None)

        digits = re.findall('\\\\?#([0-9]+),\\\\?#', line)[0]
        rounded_value = format(value, ',.%sf' % digits)
        line = re.sub('(.*?)\\\\?#[0-9]+,\\\\?#', r'\g<1>' + rounded_value, line)

    return(line)


def _insert_tables_lyx(template, tables):
    """Fill tables for LyX template.
    
    Parameters
    ----------
    template : str
        Path of LyX template to fill.
    tables : dict
        Dictionary ``{tag: values}`` of tables.

    Returns
    -------
    template : str
        Filled LyX template.
    """

    with open(template, 'r') as f:
        doc = f.readlines()
      
    is_table = False

    for i in range(len(doc)):
        if re.match('name "tab:', doc[i]):
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
                    doc[i] = _insert_value(doc[i], values[entry_count], 'no change')
                    entry_count += 1
                    break
                elif re.match('.*#[0-9]+#', doc[i]):
                    doc[i] = _insert_value(doc[i], values[entry_count], 'round')
                    entry_count += 1
                    break
                elif re.match('.*#[0-9]+,#', doc[i]):
                    doc[i] = _insert_value(doc[i], values[entry_count], 'comma + round')
                    entry_count += 1
                    break
                elif re.match('</lyxtabular>', doc[i]):
                    is_table = False
                    if entry_count != len(values):
                        raise_from(CritError(messages.crit_error_too_many_values % tag), None)
                else:
                    break
            except IndexError:
                raise_from(CritError(messages.crit_error_not_enough_values % tag), None)
                

    doc = '\n'.join(doc)
    return(doc)


def _insert_tables_latex(template, tables):
    """Fill tables for LaTeX template.
    
    Parameters
    ----------
    template : str
        Path of LaTeX template to fill.
    tables : dict
        Dictionary ``{tag: values}`` of tables.

    Returns
    -------
    template : str
        Filled LaTeX template.
    """

    with open(template, 'r') as f:
        doc = f.readlines()

    is_table = False

    for i in range(len(doc)):
        if re.search('label\{tab:', doc[i]):
            tag = doc[i].split(':')[1].rstrip('}\n').strip('"').lower()

            try:
                values = tables[tag]
                entry_count = 0
                is_table = True
            except KeyError:
                pass

        while is_table:
            line_col = doc[i].split("&")

            for j in range(len(line_col)):
                if re.search('.*\\\\#\\\\#\\\\#', line_col[j]):
                    line_col[j] = _insert_value(line_col[j], values[entry_count], 'no change')
                    entry_count += 1
                elif re.search('.*\\\\#[0-9]+\\\\#', line_col[j]):
                    line_col[j] = _insert_value(line_col[j], values[entry_count], 'round')                   
                    entry_count += 1
                elif re.search('.*\\\\#[0-9]+,\\\\#', line_col[j]):
                    line_col[j] = _insert_value(line_col[j], values[entry_count], 'comma + round')
                    entry_count += 1
               
            doc[i] = "&".join(line_col)

            if re.search('end\{tabular\}', doc[i], flags = re.IGNORECASE):
                is_table = False
                if entry_count != len(values):
                    raise_from(CritError(messages.crit_error_too_many_values % tag), None)
            else:
                break

    doc = '\n'.join(doc)

    return(doc)


def _insert_tables(template, tables):
    """Fill tables for template.
    
    Parameters
    ----------
    template : str
        Path of template to fill.
    tables : dict
        Dictionary ``{tag: values}`` of tables.

    Returns
    -------
    template : str
        Filled template.
    """
    
    if re.search('\.lyx', template):
        doc = _insert_tables_lyx(template, tables)
    elif re.search('\.tex', template):
        doc = _insert_tables_latex(template, tables)

    return(doc)


def tablefill(inputs, template, output, null = None):
    """.. Fill tables for template using inputs.
    
    Fills tables in document ``template`` using files list ``inputs``. Writes filled document to file ``output``. Null characters (i.e., ``''``, ``'.'``, ``'NA'``) in ``inputs`` are replaced with value ``null``.

    Parameters
    ----------
    inputs : list
        List of inputs to fill into template.
    template : str
        Path of template to fill.
    output : str
        Path of output.
    null : str
        Value to replace null characters (i.e., ``''``, ``'.'``, ``'NA'``). Defaults to ``None``.

    Returns
    -------
    None
    """

    try:
        if type(inputs) is not list:
            raise_from(TypeError(messages.type_error_dir_list % inputs), None)
        inputs = [norm_path(file) for file in inputs]
        content = [_parse_content(file, null) for file in inputs]
        tables = {tag:data for (tag, data) in content}

        if (len(content) != len(tables)):
            raise_from(CritError(messages.crit_error_duplicate_tables), None)

        doc = _insert_tables(template, tables) 
        
        with open(output, 'w') as f:
            f.write(doc)
    except:
        error_message = 'Error with `tablefill`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        raise_from(ColoredError(error_message, traceback.format_exc()), None)