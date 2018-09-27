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
from gslab_make_dev.private.programdirective import Directive, ProgramDirective, SASDirective, LyXDirective
from gslab_make_dev.private.utility import format_error
from gslab_make_dev.write_logs import write_to_makelog


def run_stata(paths, **kwargs):
    """ Run Stata script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `False`.
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

    makelog = paths['makelog']

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
    
    
def run_matlab(paths, **kwargs):
    """ Run Matlab script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `False`.
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
  
    makelog = paths['makelog']

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
        

def run_perl(paths, **kwargs):
    """ Run Perl script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `False`.
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
    
    makelog = paths['makelog']

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


def run_python(paths, **kwargs):
    """ Run Python script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `False`.
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
    
    makelog = paths['makelog']

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
        

def run_mathematica(paths, **kwargs):
    """ Run Mathematica script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `False`.
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
    
    makelog = paths['makelog']

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
        

def run_stat_transfer(paths, **kwargs):
    """ Run StatTransfer script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `False`.
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
    
    makelog = paths['makelog']

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
        

def run_lyx(paths, **kwargs): 
    """ Run LyX script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
            'pdf_dir' : str
                Directory to write PDFs.
        }
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `False`.
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
        
    Returns
    -------
    None
    """
    
    makelog = paths['makelog']
    pdf_dir = paths['pdf_dir']

    try:
        direct = LyXDirective(application = 'lyx', makelog = makelog, pdf_dir = pdf_dir, **kwargs)
            
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
        output_pdf = os.path.join(direct.pdf_dir, direct.program_name + '.pdf')

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
        

def run_r(paths, **kwargs):
    """ Run R script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `False`.
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
    
    makelog = paths['makelog']

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
        

def run_sas(paths, **kwargs):
    """ Run SAS script using system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `False`.
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

    makelog = paths['makelog']

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
        

def execute_command(paths, command, **kwargs):
    """ Run system command.

    Parameters
    ----------
    paths : dict 
        Dictionary of paths. Dictionary should contain {
            'makelog' : str
                Path of makelog.
        }
    command : str
        system command to run.
    osname : str, optional
        Name of OS. Defaults to `os.name`.
    shell : bool, optional
        See: https://docs.python.org/2/library/subprocess.html#frequently-used-arguments.
        Defaults to `False`.
    log : str, optional
        Path of system command log. system command log is only written if specified. 
        
    Returns
    -------
    None
    """
    
    makelog = paths['makelog']

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
        