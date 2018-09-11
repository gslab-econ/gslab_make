#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import shutil
import fileinput

import gslab_make_dev.private.metadata as metadata
from gslab_make_dev.private.programdirective import Directive, ProgramDirective, SASDirective, LyxDirective
from write_logs import write_error

def run_stata(**kwargs):
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
        directive = ProgramDirective(application = 'stata', **kwargs)

        # Get program output
        program_log = os.path.join(os.getcwd(), directive.program_name + '.log')

        # Execute
        command = metadata.commands[directive.osname]['stata'] % (directive.executable, directive.option, directive.program)
        directive.execute_command(command)
        directive.write_log()
        directive.move_program_output(program_log, directive.log)       
    except Exception as error:
        write_error("Error with run_stata: \n" + error)
        raise Exception


def run_matlab(**kwargs):
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
        directive = ProgramDirective(application = 'matlab', **kwargs)
        
        # Get program output
        program_log = os.path.join(os.getcwd(), directive.program_name + '.log')

        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.option, directive.program, directive.program_name + '.log')
        directive.execute_command(command)    
        directive.move_program_output(program_log, directive.log)       
    except Exception as error:
        write_error("Error with run_matlab: \n" + error)
        raise Exception
        

def run_perl(**kwargs):
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
        directive = ProgramDirective(application = 'perl', **kwargs)
        
        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.option, directive.program, directive.args)
        directive.execute_command(command)
        directive.write_log()
    except Exception as error:
        write_error("Error with run_perl: \n" + error)
        raise Exception


def run_python(**kwargs):
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
        directive = ProgramDirective(application = 'python', **kwargs)

        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.option, directive.program, directive.args)
        directive.execute_command(command)
        directive.write_log()
    except Exception as error:
        write_error("Error with run_python: \n" + error)
        raise Exception
        

def run_mathematica(**kwargs):
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
        directive = ProgramDirective(application = 'math', **kwargs)

        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.program, directive.option)
        directive.execute_command(command)
        directive.write_log()
    except Exception as error:
        write_error("Error with run_mathematica: \n" + error)
        raise Exception
        

def run_stat_transfer(**kwargs):
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
        directive = ProgramDirective(application = 'st', **kwargs)

        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.program)
        directive.execute_command(command)
        directive.write_log()
    except Exception as error:
        write_error("Error with run_stat_transfer: \n" + error)
        raise Exception
        

def run_lyx(**kwargs): 
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
        directive = LyxDirective(application = 'lyx', **kwargs)
            
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
        write_error("Error with run_lyx: \n" + error)
        raise Exception
        

def run_r(**kwargs):
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
        directive = ProgramDirective(application = 'r', **kwargs)

        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.option, directive.program)
        directive.execute_command(command)
        directive.write_log()      
    except Exception as error:
        write_error("Error with run_r: \n" + error)
        raise Exception
        

def run_sas(**kwargs):
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
        directive = SASDirective(application = 'sas', **kwargs)

        # Get program outputs
        program_log = os.path.join(os.getcwd(), directive.program_name + '.log')
        program_lst = os.path.join(os.getcwd(), directive.program_name + '.lst')
        
        # Execute
        command = metadata.commands[directive.osname][directive.application] % (directive.executable, directive.option, directive.program)       
        directive.execute_command(command)
        directive.move_program_output(program_log)
        directive.move_program_output(program_lst)        
    except Exception as error:
        write_error("Error with run_sas: \n" + error)
        raise Exception
        

def execute_command(command, **kwargs):
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
        directive = Directive(**kwargs)

        # Execute
        directive.execute_command(command)
        directive.write_log()   
    except Exception as error:
        write_error("Error with execute_command: \n" + error)
        raise Exception
        