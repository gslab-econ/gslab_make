import os
import shutil
import fileinput

def run_stata(**kwargs):

    try:
        run = ProgramDirective(**kwargs)

        # Get program output
        program_log = os.path.join(run.program_path, run.program_name + '.log')

        # Execute
        command = metadata.commands['stata'] % (run.executable, run.option, run.program)
        run.execute_command(command)
        run.move_program_output(program_log, run.log)
		
    except:
        print("ERROR")


def run_matlab(**kwargs)

    try:
        run = ProgramDirective(**kwargs)
        
        # Get program output
        program_log = os.path.join(run.program_path, run.program_name + '.log')

        # Execute
        command = metadata.commands['matlab'] % (run.executable, run.option, run.program, run.program_name + '.log')
        run.execute_command(command)
        run.move_program_output(program_log, run.log)
		
    except:
        print("ERROR")


def run_perl(**kwargs):

    try:
        run = ProgramDirective(**kwargs)
        
        # Execute
        command = metadata.commands['perl'] % (run.executable, run.option, run.program, run.args)
        run.execute_command(command)
    except:
        print("ERROR")


def run_python(**kwargs):

    try:
        run = ProgramDirective(**kwargs)

        # Execute
        command = metadata.commands['python'] % (run.executable, run.option, run.program, run.args)
        run.execute_command(command)
    except:
        print("ERROR")


def run_mathematica(**kwargs):

    try:
        run = ProgramDirective(**kwargs)

        # Execute
        command = metadata.commands['math'] % (run.executable, run.program, run.option)
        run.execute_command(command)
    except:
        print("ERROR")


def run_stat_transer(**kwargs):

    try:
        run = ProgramDirective(**kwargs)

        # Execute
        command = metadata.commands['st'] % (run.executable, run.program)
        run.execute_command(command)
    except:
        print("ERROR")


def run_lyx(**kwargs): # Check
    """
	Export a LyX file to PDF

    Example: 
	    To create PDF for 'draft.lyx', use command:
        `run_lyx(program = 'draft.lyx')`
    """

    try:
        run = ProgramDirective(**kwargs)
            
        # Make handout/commented LyX file
        handout = run.handout
        comments = run.comments

		if handout:
		    suffix = '_handout'
		else if comments: 
		    suffix = '_comments'		
		
        if handout or comments:
            temp_program_name = os.path.join(run.program_name + suffix)
            temp_program  = os.path.join(run.program_path, temp_program_name + '.lyx') 
            
            beamer = False
            shutil.copy2(run.program, temp_program) 
            for line in fileinput.input(temp_program, inplace = True):
                if r'\textclass beamer' in line:
                    beamer = True
                elif handout and r'\options' in line and beamer:
                    line = line.rstrip('\n') + ', handout\n'
                elif comments and r'\begin_inset Note Note' in line:
                    line = line.replace('Note Note', 'Note Greyedout')
        else:
             temp_program_name = run.program_name
             temp_program = run.program

        # Execute
        command = metadata.commands['lyx'] % (run.executable, run.option, temp_program)
        run.execute_command(command)

        # Move PDF output
        pdf_name = os.path.join(run.program_path, temp_program_name + '.pdf')
        pdf_out = run.pdf_out
		
        if pdf_name != pdf_out:
            shutil.copy2(pdf_name, pdf_out)
            os.remove(pdf_name)
            
        # Remove handout/commented LyX file
        if handout or comments:
            os.remove(temp_program)

    except:
        print("ERROR")


def run_r(**kwargs):

    try:
        run = ProgramDirective(**kwargs)

        # Execute
        command = metadata.commands['r'] % (run.executable, run.option, run.program)
        run.execute_command(command)
        run.move_program_output(program_log, run.log)
		
    except:
        print("ERROR")


def run_sas(**kwargs):
    try:
        run = ProgramDirective(**kwargs)

	    # Get program outputs
        program_log = os.path.join(run.program_path, run.program_name + '.log')
        program_lst = os.path.join(run.program_path, run.program_name + '.lst')
		
        # Execute
        command = metadata.commands['sas'] % (run.executable, run.option, run.program)       
        run.execute_command(command)
        run.move_program_output(default_log)
        run.move_program_output(default_lst)
		
    except:
        print("ERROR")


def execute_command(command, **kwargs):
    """
	Run a shell command
	"""

    try:
	    run = RunDirective(**kwargs)
		
		# Execute
		run.execute_run(command)
	
    except:
        print("ERROR")
