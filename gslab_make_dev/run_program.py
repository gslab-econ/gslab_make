#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import shutil
import fileinput
import traceback

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
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.

    Returns
    -------
    None
    """

    try:
        direct = ProgramDirective(application = 'stata', makelog = makelog, **kwargs)

        # Get program output
        program_log = os.path.join(os.getcwd(), direct.program_name + '.log')

        # Execute
        command = metadata.commands[direct.osname]['stata'] % (direct.executable, direct.option, direct.program)
        exit_code, error_message = direct.execute_command(command)
        direct.write_log()
        direct.move_program_output(program_log, direct.log)  
        if exit_code != 0:
            raise CritError('* Stata program executed with errors: *\n%s' % error_message)
    except:
        error_message = 'Error with `run_stata`' 
        error_message = format_error(error_message) + '\n' + traceback.format_exc()
        write_to_makelog(error_message, makelog)
        raise
    
    
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
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.

    Returns
    -------
    None
    """
    
    try:
        direct = ProgramDirective(application = 'matlab', makelog = makelog, **kwargs)
        
        # Get program output
        program_log = os.path.join(os.getcwd(), direct.program_name + '.log')

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, direct.program, direct.program_name + '.log')
        exit_code, error_message = direct.execute_command(command)    
        direct.move_program_output(program_log, direct.log)   
        if exit_code != 0:
            raise CritError('* Matlab program executed with errors: *\n%s' % error_message)
    except:
        error_message = 'Error with `run_matlab`' 
        error_message = format_error(error_message) + '\n' + traceback.format_exc()
        write_to_makelog(error_message, makelog)
        raise
        

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
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Arguments for system command. Defaults to no arguments.

    Returns
    -------
    None
    """
    
    try:
        direct = ProgramDirective(application = 'perl', makelog = makelog, **kwargs)
        
        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, direct.program, direct.args)
        exit_code, error_message = direct.execute_command(command)
        direct.write_log()
        if exit_code != 0:
            raise CritError('* Perl program executed with errors: *\n%s' % error_message)
    except:
        error_message = 'Error with `run_perl`' 
        error_message = format_error(error_message) + '\n' + traceback.format_exc()
        write_to_makelog(error_message, makelog)
        raise


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
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Arguments for system command. Defaults to no arguments.

    Returns
    -------
    None
    """
    
    try:
        direct = ProgramDirective(application = 'python', makelog = makelog, **kwargs)

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, direct.program, direct.args)
        exit_code, error_message = direct.execute_command(command)
        direct.write_log()
        if exit_code != 0:
            raise CritError('* Python program executed with errors: *\n%s' % error_message)
    except:
        error_message = 'Error with `run_python`' 
        error_message = format_error(error_message) + '\n' + traceback.format_exc()
        write_to_makelog(error_message, makelog)
        raise
        

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
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.
        
    Returns
    -------
    None
    """
    
    try:
        direct = ProgramDirective(application = 'math', makelog = makelog, **kwargs)

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.program, direct.option)
        exit_code, error_message = direct.execute_command(command)
        direct.write_log()
        if exit_code != 0:
            raise CritError('* Mathematica program executed with errors: *\n%s' % error_message)
    except:
        error_message = 'Error with `run_mathematica`' 
        error_message = format_error(error_message) + '\n' + traceback.format_exc()
        write_to_makelog(error_message, makelog)
        raise
        

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
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.

    Returns
    -------
    None
    """
    
    try:
        direct = ProgramDirective(application = 'st', makelog = makelog, **kwargs)

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.program)
        exit_code, error_message = direct.execute_command(command)
        direct.write_log()
        if exit_code != 0:
            raise CritError('* StatTransfer program executed with errors: *\n%s' % error_message)
    except:
        error_message = 'Error with `run_stat_transfer`' 
        error_message = format_error(error_message) + '\n' + traceback.format_exc()
        write_to_makelog(error_message, makelog)
        raise
        

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
        Executable to use for system command. 
        Defaults to executable specified in metadata.
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
        direct = LyxDirective(application = 'lyx', makelog = makelog, **kwargs)
            
        # Make handout/commented LyX file        
        if direct.doctype:
            temp_name = os.path.join(direct.program_name + '_' + direct.doctype)
            temp_program = os.path.join(direct.program_dir, temp_name + '.lyx') 
            
            beamer = False
            shutil.copy2(direct.program, temp_program) 

            for line in fileinput.input(temp_program, inplace = True):
                if r'\textclass beamer' in line:
                    beamer = True          
                if direct.doctype == 'handout' and r'\options' in line and beamer:
                    line = line.rstrip('\n') + ', handout\n'
                elif direct.doctype == 'comments' and r'\begin_inset Note Note' in line:
                    line = line.replace('Note Note', 'Note Greyedout')
                print(line)
        else:
            temp_name = direct.program_name
            temp_program = direct.program

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, temp_program)
        exit_code, error_message = direct.execute_command(command)
        direct.write_log()
        if exit_code != 0:
            raise CritError('* LyX program executed with errors: *\n%s' % error_message)

        # Move PDF output
        temp_pdf = os.path.join(direct.program_dir, temp_name + '.pdf')
        output_pdf = os.path.join(direct.pdfout, direct.program_name + '.pdf')

        if temp_pdf != output_pdf:
            shutil.copy2(temp_pdf, output_pdf)
            os.remove(temp_pdf)
            
        # Remove handout/commented LyX file
        if direct.doctype:
            os.remove(temp_program)
    except:
        error_message = 'Error with `run_lyx`' 
        error_message = format_error(error_message) + '\n' + traceback.format_exc()
        write_to_makelog(error_message, makelog)
        raise
        

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
        Executable to use for system command. 
        Defaults to executable specified in metadata.
    option : str, optional
        Options for system command. Defaults to options specified in metadata.
    args : str, optional
        Not applicable.

    Returns
    -------
    None
    """
    
    try:
        direct = ProgramDirective(application = 'r', makelog = makelog, **kwargs)

        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, direct.program)
        exit_code, error_message = direct.execute_command(command)
        direct.write_log()      
        if exit_code != 0:
            raise CritError('* R program executed with errors: *\n%s' % error_message)
    except:
        error_message = 'Error with `run_r`' 
        error_message = format_error(error_message) + '\n' + traceback.format_exc()
        write_to_makelog(error_message, makelog)
        raise
        

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
        Executable to use for system command. 
        Defaults to executable specified in metadata.
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
        direct = SASDirective(application = 'sas', makelog = makelog, **kwargs)

        # Get program outputs
        program_log = os.path.join(os.getcwd(), direct.program_name + '.log')
        program_lst = os.path.join(os.getcwd(), direct.program_name + '.lst')
        
        # Execute
        command = metadata.commands[direct.osname][direct.application] % (direct.executable, direct.option, direct.program)       
        exit_code, error_message = direct.execute_command(command)
        direct.move_program_output(program_log)
        direct.move_program_output(program_lst)        
        if exit_code != 0:
            raise CritError('* SAS program executed with errors: *\n%s' % error_message)
    except:
        error_message = 'Error with `run_sas`' 
        error_message = format_error(error_message) + '\n' + traceback.format_exc()
        write_to_makelog(error_message, makelog)
        raise
        

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
        direct = Directive(makelog = makelog, **kwargs)

        # Execute
        exit_code, error_message = direct.execute_command(command)
        direct.write_log()   
        if exit_code != 0:
            raise CritError('* Command executed with errors: *\n%s' % error_message)
    except:
        error_message = 'Error with `execute_command`' 
        error_message = format_error(error_message) + '\n' + traceback.format_exc()
        write_to_makelog(error_message, makelog)
        raise
        