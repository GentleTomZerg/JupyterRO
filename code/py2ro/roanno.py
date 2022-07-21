import inspect
from rocrate.model.contextentity import ContextEntity
from rocrate.rocrate import ROCrate

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

def cell(func):
    def toRO():
        global jupyter_notebook
        global count
        # do not count duplicate func
        if inspect.getsource(func) in func_list:
            return toRO
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
        
        # call the func
        # TODO: call func with parameters
        cell1 = crate.add(
            Cell(crate, str(count + 2), properties={
                "content": func.__name__ + "()",
            }))

        cells.append(md_cell)
        cells.append(cell)
        cells.append(cell1)
        count += 3
        
        func()
        #add func into func_list, avoid duplicates
        func_list.append(inspect.getsource(func))

    return toRO


def rocrate(func):
    def jsonify():
        func()
        jupyter_notebook["cells"] = cells
        crate.write("../../result/test")

    return jsonify

# TODO: make cells be a linked list, which supports remove, insert and delete 