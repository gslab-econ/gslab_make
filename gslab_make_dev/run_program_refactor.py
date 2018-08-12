import os
import shutil
import fileinput

def run_stata(**kwargs):

    try:
        run = ProgramDirective(**kwargs)
        run.check_os()
        run.check_program('stata')

        # Set option
        option = run.option
        if not option:
            if run.osname == 'posix':
                option = metadata.default_options['stataunix']
            else if run.osname == 'nt':
                option = metadata.default_options['statawin']

        # Get program output
        program_log = os.path.join(run.program_path, run.program_name + '.log')

        # Execute
        command = metadata.commands['stata'] % (run.executable, option, run.program)
        run.run_command(command)
        run.move_program_output(program_log, run.log)
    except:
        ERROR


def run_matlab(**kwargs)
    try:
        run = RunProgramDirective(kwargs)
        run.check_os()
        run.check_program('matlab')

        # Get option
        option = run.option
        if not option:
            if run.osname == 'posix':
                option = metadata.default_options['matlabunix']
            else if run.osname == 'nt':
                option = metadata.default_options['matlabwin']
        
        # GEt program output
        program_log = os.path.join(run.program_path, run.program_name + '.log')

        # Execute
        command = metadata.commands['matlab'] % (run.executable, run.program, run.program_name + '.log', option)
        run.run_command(command)
        run.move_program_output(program_log, run.log)
    except:
        ERROR


def run_perl(**kwargs):
    """Execute a Perl script"""

    try:
        run = RunProgramDirective(kwargs)
        run.check_os()
        run.check_program('perl')
        
        # Execute
        command = metadata.commands['perl'] % (run.executable, run.option, run.program, run.args)
        run.run_command(command)
    except:
        ERROR


def run_python(**kwargs):
    """Execute a Python script."""

    try:
        run = RunProgramDirective(kwargs)
        run.check_os()
        run.check_program('python')

        # Execute
        command = metadata.commands['python'] % (run.executable, run.option, run.program, run.args)
        run.run_command(command)
    except:
        ERROR


def run_mathematica(**kwargs):
    """Execute a Mathematica script"""

    try:
        run = RunProgramDirective(kwargs)
        run.check_os()
        run.check_program('math')
       
        # Get option
        option = run.option
        if not option:
            option = metadata.default_options['math']

        # Execute
        command = metadata.commands['math'] % (run.executable, run.program, option)
        run.run_command(command)
    except:
        ERROR


def run_stc(**kwargs):
    """Run StatTransfer .stc program"""

    try:
        run = RunProgramDirective(kwargs)
        run.check_os()
        run.check_program('stc')

        # Execute
        command = metadata.commands['st'] % (run.executable, program)
        run.run_command(command)
    except:
        ERROR


def run_stcmd(**kwargs):
    """Run StatTransfer .stcmd program"""

    try:
        run = RunProgramDirective(kwargs)
        run.check_os()
        run.check_program('stcmd')

        # Execute
        command = metadata.commands['st'] % (run.executable, program)
        run.run_command(command)
    except:
        ERROR


def run_lyx(**kwargs):
    """Export a LyX file to PDF

    e.g. To create pdf file for 'draft.lyx' with the log file being './make.log',
         use the command:
        `run_lyx(program = 'draft', makelog = './make.log')`
    """

    try:
        run = RunProgramDirective(kwargs)
        run.error_check('lyx')
        program_name = run.program_name
        if run.changedir:
            program = '"' + run.program + '"'
        else:
            program = '"' + run.program_full + '"'
        
        # Get option
        option = run.option
        if not run.option:
            option = metadata.default_options['lyx']
            
        # Make handout/commented LyX file
        handout = run.handout
        comments = run.comments

        if handout or comments:
            program_name_suffix = '_handout' if handout else '_comments'
            temp_program_name = program_name + program_name_suffix
            temp_program_full = os.path.join(run.program_path, temp_program_name + '.lyx') 
            
            program = program.replace(program_name, temp_program_name)
            program_name = temp_program_name
            
            beamer = False
            shutil.copy2(run.program_full, temp_program_full)
            for line in fileinput.input(temp_program_full, inplace = True):
                if r'\textclass beamer' in line:
                    beamer = True
                elif handout and r'\options' in line and beamer:
                    line = line.rstrip('\n') + ', handout\n'
                elif comments and r'\begin_inset Note Note' in line:
                    line = line.replace('Note Note', 'Note Greyedout')
                print line,
        
        # Get executable
        executable = run.executable
        if not run.executable:
            executable = metadata.default_executables['lyx']

        command = metadata.commands['lyx'] % (executable, option, program)

        run.execute_run(command)

        # Move PDF output
        pdfname = os.path.join(run.program_path, program_name + '.pdf')
        pdfout = run.pdfout
        if not '.pdf' in pdfout:
            pdfout = os.path.join(pdfout, program_name + '.pdf')
        if os.path.abspath(pdfname) != os.path.abspath(pdfout):
            shutil.copy2(pdfname, pdfout)
            os.remove(pdfname)
            
        # Remove handout/commented LyX file
        if handout or comments:
            os.remove(temp_program_full)

    except:
        add_error_to_log(run.makelog)


def run_rbatch(**kwargs):
    """Run an R batch program with log file"""

    try:
        run = RunProgramDirective(kwargs)
        run.error_check('rbatch')

        # Get option
        option = run.option
        if not run.option:
            option = metadata.default_options['rbatch']
        if run.changedir:
            program = '"' + run.program + '"'
            default_log = os.path.join(run.program_path, run.program_name + '.Rout')
        else:
            program = '"' + os.path.join(run.program_path, run.program) + '"'
            default_log = os.path.join(os.getcwd(), run.program_name + '.Rout')

        # Get executable
        executable = run.executable
        if not run.executable:
            executable = metadata.default_executables['rbatch']

        command = metadata.commands['rbatch'] % (executable, option, program, run.program_name + '.Rout')

        run.execute_run(command)
        run.move_log(default_log)
    except:
        ERROR


def run_sas(**kwargs):
    """Run a SAS script"""

    try:
        run = RunProgramDirective(kwargs)
        run.error_check('sas')

        # Get option
        option = run.option
        if not run.option:
            if run.osname != 'posix':
                option = metadata.default_options['saswin']

        # Get executable
        executable = run.executable
        if not run.executable:
            executable = metadata.default_executables['sas']

        # Get log, lst, and program
        if run.changedir:
            program = '"' + run.program + '"' 
            default_log = os.path.join(run.program_path, run.program_name + '.log')
            default_lst = os.path.join(run.program_path, run.program_name + '.lst')
        else:
            program = '"' + os.path.join(run.program_path, run.program) + '"'
            default_log = os.path.join(os.getcwd(), run.program_name + '.log')
            default_lst = os.path.join(os.getcwd(), run.program_name + '.lst')


        if run.osname == 'posix':
            command = metadata.commands['sas'] % (executable, option, program)
        else:
            command = metadata.commands['sas'] % (executable, program, option)

        run.execute_run(command)
        run.move_log(default_log)
        run.move_lst(default_lst)
    except:
        ERROR


def run_command(**kwargs):
    """Run a Shell command"""
    
    run = RunCommandDirective(kwargs)
    try:
        run.error_check('other')
        run.execute_run(run.command)
    except:
        ERROR
