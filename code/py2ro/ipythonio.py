from IPython.core.interactiveshell import InteractiveShell
from IPython.utils import capture
from IPython.utils.io import capture_output
a=InteractiveShell()
code = "print(1)"

with capture_output() as out:
    a.run_cell(code)
print(out)    