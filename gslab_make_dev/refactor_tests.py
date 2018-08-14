# Modules
import os 
os.chdir("/Users/zong/gslab_make/gslab_make_dev")
import run_program

# Start make log
run_program.metadata.makelog_started = True

# Tests
run_program.run_matlab(program = "_tests/matlab.m", log = "_tests/matlab.log")

run_program.run_python(program = "_tests/python.py", log = "_tests/python.log")

run_program.run_r(program = "_tests/r.R", log = "_tests/r.log")

run_program.run_stata(program = "_tests/stata.do", log = "_tests/stata.log")

run_program.execute_command(command = "ls", log = "_tests/command.log")