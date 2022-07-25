import inspect
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils import capture
from IPython.utils.io import capture_output
shell=InteractiveShell()
def a():
    print("Process a");

with capture_output() as out:
    shell.run_cell(" ".join(inspect.getsourcelines(a)[0]))
    shell.run_cell(a.__name__ + "()")

# with capture_output() as out:
#     shell.run_cell("print('1')")
#     # shell.run_cell(a.__name__ + "()")    
print(out)    