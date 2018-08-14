# Modules
import os 
os.chdir("/Users/zong/gslab_make/gslab_make_dev")
import run_program

# Start make log
run_program.metadata.makelog_started = True

# Tests
run_program.run_matlab(program = "refactor_tests/matlab.m", log = "refactor_tests/matlab.log")

run_program.run_python(program = "refactor_tests/python.py", log = "refactor_tests/python.log")

run_program.run_r(program = "refactor_tests/r.R", log = "refactor_tests/r.log")

run_program.run_stata(program = "refactor_tests/stata.do", log = "refactor_tests/stata.log")

run_program.execute_command(command = "ls", log = "refactor_tests/command.log")