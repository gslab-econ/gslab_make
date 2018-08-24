# Modules
import os 
os.chdir("/Users/zong/gslab_make/gslab_make_dev")

import run_program
import dir_mod
import make_link_logs
import make_links
import make_logs

# Clear directories
dir_mod.clear_dir('input', 'output')
dir_mod.remove_path('input')
# Start make log

# Tests
run_program.run_matlab(program = "_tests/matlab.m", log = "_tests/matlab.log")

run_program.run_python(program = "_tests/python.py", log = "_tests/python.log")

run_program.run_r(program = "_tests/r.R", log = "_tests/r.log")

run_program.run_stata(program = "_tests/stata.do", log = "_tests/stata.log")

run_program.execute_command(command = "ls", log = "_tests/command.log")


def norm_path(path):
    path = re.split('[/\\\\]+', path)
    path = [p if p else os.path.sep for p in path]
    path = os.path.join(*path)
    path = os.path.abspath(path)

    return(path)
