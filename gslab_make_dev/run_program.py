#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import shutil
import fileinput

import gslab_make_dev.private.metadata as metadata
from gslab_make_dev.private.exceptionclasses import CritError
from gslab_make_dev.private.programdirective import Directive, ProgramDirective, SASDirective, LyxDirective
from gslab_make_dev.private.utility import format_error
from gslab_make_dev.write_logs import write_to_makelog


def run_stata(makelog = metadata.settings['makelog'], **kwargs):
    """ Run Stata script using system command.

    Parameters
    ----------
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `False`.
    makelog : str, optional
        Path of makelog. Defaults to path specified in metadata.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    program : str
        Path of script to run.
    executable : str, optional
        Executable to use for system command. Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.

    Returns
    -------
    None
    """

    try:
        directive = ProgramDirective(application = 'stata', makelog = makelog, **kwargs)

        # Get program output
        program_log = os.path.join(os.getcwd(), directive.program_name + '.log')

        # Execute
        command = metadata.commands[directive.osname]['stata'] % (directive.executable, directive.option, directive.program)
        directive.execute_command(command)
        directive.write_log()
        directive.move_program_output(program_log, directive.log)       
    except Exception as error:
        error = format_error('Error with `run_stata`: \n' + str(error))
        write_to_makelog(error, makelog)
        raise CritError(error)
    
    
def run_matlab(makelog = metadata.settings['makelog'], **kwargs):
    """ Run Matlab script using system command.

    Parameters
    ----------
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `False`.
    makelog : str, optional
        Path of makelog. Defaults to path specified in metadata.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    program : str
        Path of script to run.
    executable : str, optional
        Executable to use for system command. Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.

    Returns
    -------
    None
    """
    
    try:
        directive = ProgramDirective(application = 'matlab', makelog = makelog, **kwargs)
        
        # Get program output
        program_log = os.path.join(os.getcwd(), directive.program_name + '.log')

        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.option, directive.program, directive.program_name + '.log')
        directive.execute_command(command)    
        directive.move_program_output(program_log, directive.log)       
    except Exception as error:
        error = format_error('Error with `run_matlab`: \n' + str(error))
        write_to_makelog(error, makelog)
        raise CritError(error)
        

def run_perl(makelog = metadata.settings['makelog'], **kwargs):
    """ Run Perl script using system command.

    Parameters
    ----------
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `False`.
    makelog : str, optional
        Path of makelog. Defaults to path specified in metadata.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    program : str
        Path of script to run.
    executable : str, optional
        Executable to use for system command. Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Arguments for system command. Defaults to no arguments.

    Returns
    -------
    None
    """
    
    try:
        directive = ProgramDirective(application = 'perl', makelog = makelog, **kwargs)
        
        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.option, directive.program, directive.args)
        directive.execute_command(command)
        directive.write_log()
    except Exception as error:
        error = format_error('Error with `run_perl`: \n' + str(error))
        write_to_makelog(error, makelog)
        raise CritError(error)


def run_python(makelog = metadata.settings['makelog'], **kwargs):
    """ Run Python script using system command.

    Parameters
    ----------
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `False`.
    makelog : str, optional
        Path of makelog. Defaults to path specified in metadata.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    program : str
        Path of script to run.
    executable : str, optional
        Executable to use for system command. Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Arguments for system command. Defaults to no arguments.

    Returns
    -------
    None
    """
    
    try:
        directive = ProgramDirective(application = 'python', makelog = makelog, **kwargs)

        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.option, directive.program, directive.args)
        directive.execute_command(command)
        directive.write_log()
    except Exception as error:
        error = format_error('Error with `run_python`: \n' + str(error))        
        write_to_makelog(error, makelog)
        raise CritError(error)
        

def run_mathematica(makelog = metadata.settings['makelog'], **kwargs):
    """ Run Mathematica script using system command.

    Parameters
    ----------
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `False`.
    makelog : str, optional
        Path of makelog. Defaults to path specified in metadata.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    program : str
        Path of script to run.
    executable : str, optional
        Executable to use for system command. Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.
        
    Returns
    -------
    None
    """
    
    try:
        directive = ProgramDirective(application = 'math', makelog = makelog, **kwargs)

        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.program, directive.option)
        directive.execute_command(command)
        directive.write_log()
    except Exception as error:
        error = format_error('Error with `run_mathematica`: \n' + str(error))        
        write_to_makelog(error, makelog)
        raise CritError(error)
        

def run_stat_transfer(makelog = metadata.settings['makelog'], **kwargs):
    """ Run StatTransfer script using system command.

    Parameters
    ----------
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `False`.
    makelog : str, optional
        Path of makelog. Defaults to path specified in metadata.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    program : str
        Path of script to run.
    executable : str, optional
        Executable to use for system command. Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.

    Returns
    -------
    None
    """
    
    try:
        directive = ProgramDirective(application = 'st', makelog = makelog, **kwargs)

        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.program)
        directive.execute_command(command)
        directive.write_log()
    except Exception as error:
        error = format_error('Error with `run_stat_transfer`: \n' + str(error))        
        write_to_makelog(error, makelog)
        raise CritError(error)
        

def run_lyx(makelog = metadata.settings['makelog'], **kwargs): 
    """ Run Lyx script using system command.

    Parameters
    ----------
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `False`.
    makelog : str, optional
        Path of makelog. Defaults to path specified in metadata.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    program : str
        Path of script to run.
    executable : str, optional
        Executable to use for system command. Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.
    doctype : str, optional
       Type of Lyx document. Takes either `handout` and `comments`. 
       Defaults to no special document type.
    pdfout : str, optional
        Directory to write PDF. Defaults to directory specified in metadata.
        
    Returns
    -------
    None
    """
    
    try:
        directive = LyxDirective(application = 'lyx', makelog = makelog, **kwargs)
            
        # Make handout/commented LyX file        
        if directive.doctype:
            temp_name = os.path.join(directive.program_name + '_' + directive.doctype)
            temp_program = os.path.join(directive.program_dir, temp_name + '.lyx') 
            
            beamer = False
            shutil.copy2(directive.program, temp_program) 
            for line in fileinput.input(temp_program, inplace = True):
                if r'\textclass beamer' in line:
                    beamer = True
                elif directive.doctype == 'handout' and r'\options' in line and beamer:
                    line = line.rstrip('\n') + ', handout\n'
                elif directive.doctype == 'comments' and r'\begin_inset Note Note' in line:
                    line = line.replace('Note Note', 'Note Greyedout')
        else:
             temp_name = directive.program_name
             temp_program = directive.program

        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.option, temp_program)
        directive.execute_command(command)
        directive.write_log()

        # Move PDF output
        temp_pdf = os.path.join(directive.program_dir, temp_name + '.pdf')
        output_pdf = os.path.join(directive.pdfout, directive.program_name + '.pdf')

        if temp_pdf != output_pdf:
            shutil.copy2(temp_pdf, output_pdf)
            os.remove(temp_pdf)
            
        # Remove handout/commented LyX file
        if directive.doctype:
            os.remove(temp_program)
    except Exception as error:
        error = format_error('Error with `run_lyx`: \n' + str(error))        
        write_to_makelog(error, makelog)
        raise CritError(error)
        

def run_r(makelog = metadata.settings['makelog'], **kwargs):
    """ Run R script using system command.

    Parameters
    ----------
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `False`.
    makelog : str, optional
        Path of makelog. Defaults to path specified in metadata.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    program : str
        Path of script to run.
    executable : str, optional
        Executable to use for system command. Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.

    Returns
    -------
    None
    """
    
    try:
        directive = ProgramDirective(application = 'r', makelog = makelog, **kwargs)

        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.option, directive.program)
        directive.execute_command(command)
        directive.write_log()      
    except Exception as error:
        error = format_error('Error with `run_r`: \n' + str(error))        
        write_to_makelog(error, makelog)
        raise CritError(error)
        

def run_sas(makelog = metadata.settings['makelog'], **kwargs):
    """ Run SAS script using system command.

    Parameters
    ----------
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `False`.
    makelog : str, optional
        Path of makelog. Defaults to path specified in metadata.
    log : str, optional
        Path of program log. Program log is only written if specified. 
    program : str
        Path of script to run.
    executable : str, optional
        Executable to use for system command. Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.
    lst : str, optional
        Path of program lst. Program lst is only written if specified. 
        
    Returns
    -------
    None
    """

    try:
        directive = SASDirective(application = 'sas', makelog = makelog, **kwargs)

        # Get program outputs
        program_log = os.path.join(os.getcwd(), directive.program_name + '.log')
        program_lst = os.path.join(os.getcwd(), directive.program_name + '.lst')
        
        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.option, directive.program)       
        directive.execute_command(command)
        directive.move_program_output(program_log)
        directive.move_program_output(program_lst)        
    except Exception as error:
        error = format_error('Error with `run_sas`: \n' + str(error))
        write_to_makelog(error, makelog)
        raise CritError(error)
        

def execute_command(command, makelog = metadata.settings['makelog'], **kwargs):
    """ Run system command.

    Parameters
    ----------
    command : str
        system command to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `False`.
    makelog : str, optional
        Path of makelog. Defaults to path specified in metadata.
    log : str, optional
        Path of system command log. system command log is only written if specified. 
        
    Returns
    -------
    None
    """
    
    try:
        directive = Directive(makelog = makelog, **kwargs)

        # Execute
        directive.execute_command(command)
        directive.write_log()   
    except Exception as error:
        error = format_error('Error with `execute_command`: \n' + str(error))        
        write_to_makelog(error, makelog)
        raise CritError(error)
        