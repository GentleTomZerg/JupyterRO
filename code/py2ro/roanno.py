from concurrent.futures import thread
import inspect
from sys import stderr, stdout
from rocrate.model.contextentity import ContextEntity
from rocrate.rocrate import ROCrate
import os.path as path;

from IPython.core.interactiveshell import InteractiveShell
from IPython.utils import capture
from IPython.utils.io import capture_output

import threading

# TODO: Do we need History record here?
# or we just let jupyter do it?
class Cell(ContextEntity):
    def __init__(self, crate, identifier=None, properties=None):
        super(Cell, self).__init__(crate, identifier, properties)

    def _empty(self):
        val = {"@id": self.id, "@type": 'cell'}
        return val


crate = ROCrate()
cells = []
jupyter_notebook = None
count = 0
file_list = [] 
func_list = []
shell = InteractiveShell()

def cell(func):
    def toRO():
        if (exist()):
            pass
        else:
            buildROCell(func)
    return toRO


def rocrate(func):
    def jsonify():
        func()
        jupyter_notebook["cells"] = cells
        crate.write("../../result/test")

    return jsonify

# TODO: make cells be a linked list, which supports remove, insert and delete 

def exist():
    return path.isfile('../../result/test')

def buildROCell(func):
    global jupyter_notebook
    global count
    # do not count duplicate func
    if inspect.getsource(func) in func_list:
        return
    # there should only be one jupyter_notebook
    if (jupyter_notebook == None):
        jupyter_notebook = crate.add_file("cells",
                                            properties={
                                                "name":
                                                "jupyter_cells"
                                            })

    # if func is in a new file, save the file in ro-crate
    if (len(file_list) == 0):
        crate.add_file(inspect.getfile(func),
                                            properties={
                                                "name":
                                                "python file",
                                                "encodingFormat":
                                                "application/json"
                                            })
        file_list.append(inspect.getfile(func))
    elif (inspect.getfile(func) not in file_list):
        crate.add_file(inspect.getfile(func),
                                            properties={
                                                "name":
                                                "python file",
                                                "encodingFormat":
                                                "application/json"
                                            })
        file_list.append(inspect.getfile(func))

    # store info in a cell without executing the func
    markdown = inspect.getcomments(func)
    md_cell = crate.add(
        Cell(crate, str(count), properties={
            # TODO: decide if we want @cell in ro-crate
            "markdown": markdown,
        }))
         
    cell = crate.add(
        Cell(crate, str(count + 1), properties={
            # TODO: decide if we want @cell in ro-crate
            "content": inspect.getsourcelines(func)[0],
        }))
    
    t = Shell(1, "shell", func)
    t.start()
    t.join()
    out = t.get_out()
    # call the func
    # TODO: call func with parameters
    cell1 = crate.add(
        Cell(crate, str(count + 2), properties={
            "content": func.__name__ + "()",
            "outputs": out.outputs,
            "stdout": out.stdout,
            "stderr": out.stderr,
        }))

    cells.append(md_cell)
    cells.append(cell)
    cells.append(cell1)
    count += 3
    
    
    # func()
    #add func into func_list, avoid duplicates
    func_list.append(inspect.getsource(func))

def existHandler():
    ro_cells = []
    crate = ROCrate('../../result/test')
    for e in crate.contextual_entities:
        ro_cells.append(e._jsonld)
    return ro_cells



class Shell(threading.Thread):
    def __init__(self, threadID, name, func):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.out = None
        self.func = func
        
    def run(self):
        self.out = self.get_output(self.func)
            
    def get_out(self):
        return self.out
    def get_output(self, func):
      # execute func() code
        with capture_output() as out:
            # (['@cell \n', 'def a():\n', '    print("Process a");\n'], 6)
            # This is the output of inspect.getsourcelines(func)
            shell.run_cell(" ".join(inspect.getsourcelines(func)[0][1:]))
            shell.run_cell(func.__name__ + "()")
        return out    
    