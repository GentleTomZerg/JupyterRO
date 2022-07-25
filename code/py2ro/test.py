import nbformat
cells = []
nb = nbformat.read("code/py2ro/jupyter.ipynb", as_version=4)
nbcells = nb.cells
for cell in nbcells:
    if cell["cell_type"] == 'markdown':
        cells.append(cell);
    elif cell["cell_type"] == 'code':
        cells.append(cell);


    

    