from rocrate.rocrate import ROCrate
from rocrate.model.person import Person
import nbformat
import base64
import re
from io import BytesIO
from PIL import Image
import argparse

alice_id = "https://orcid.org/0000-0000-0000-0000"
bob_id = "https://orcid.org/0000-0000-0000-0001"

from rocrate.model.contextentity import ContextEntity

class Cell(ContextEntity):

    def __init__(self, crate, identifier=None, properties=None):
        super(Cell, self).__init__(crate, identifier, properties)

    def _empty(self):
        val = {
            "@id": self.id,
            "@type": 'cell'
        }
        return val

class Output(ContextEntity):

    def __init__(self, crate, identifier=None, properties=None):
        super(Cell, self).__init__(crate, identifier, properties)

    def _empty(self):
        val = {
            "@id": self.id,
            "@type": 'output'
        }
        return val

class JupyterCells2RO():
    def __init__(self) -> None:
        self.cells = []
        self.crate = ROCrate()

    def get_cells(self, filename):
        nb = nbformat.read(filename, as_version=4)
        cells = nb.cells
        for cell in cells:
            if cell["cell_type"] == 'markdown':
                self.cells.append(cell);
            elif cell["cell_type"] == 'code':
                self.cells.append(cell);
                # outputs = cell["outputs"]
                # if len(outputs) > 0:
                #     print(outputs[0]) 

    def buildCellsRO(self, filename):
        # add data entities
        jupyter_notebook = self.crate.add_file(filename,
                                          properties={
                                              "name": "jupyternotebook",
                                              "encodingFormat": "application/json"
                                          })
        # transfer jupyter cells into RO-cells
        ro_cells = []
        for i in range(len(self.cells)):
            if self.cells[i]["cell_type"] == 'markdown':
                cell_id = "markdown_cell" + str(i)
                ro_cell = self.crate.add(
                Cell(self.crate,
                    cell_id,
                    properties={
                        "content": self.cells[i]["source"],
                    }))
            elif self.cells[i]["cell_type"] == 'code':
                cell_id = "code_cell-" + str(i)
                ro_cell = self.crate.add(
                Cell(self.crate,
                    cell_id,
                    properties={
                        "content": self.cells[i]["source"],
                    }))
                outputs = self.buildOutputRO(self.cells[i]["outputs"], str(i))
                ro_cell["outputs"] = outputs
                if "cell-" + str(i) + '.png' in outputs:
                    ro_cell["outputs"] = self.crate.add_file("cell-" + str(i) + '.png',
                                                properties={
                                                    "name": "output-image",
                                                    "encodingFormat": "image/png"
                                                })       
                ro_cells.append(ro_cell)                

        # add contextual data entities
        alice = self.crate.add(
            Person(self.crate,
                   alice_id,
                   properties={
                       "name": "Alice Doe",
                       "affiliation": "University of Manchester"
                   }))
        bob = self.crate.add(
            Person(self.crate,
                   bob_id,
                   properties={
                       "name": "Bob Doe",
                       "affiliation": "University of Manchester"
                   }))

        jupyter_notebook["author"] = [alice, bob]
        jupyter_notebook["cells"] = ro_cells

        self.crate.write("result/" + filename + "crate")           

    def buildOutputRO(self, outputs, count):
        res = []
        for output in outputs:
            if "data" in output.keys():
                # handle data to image
                data = output["data"]
                if "image/png" in data.keys():
                    base64_data = data["image/png"]
                    byte_data = base64.b64decode(base64_data)
                    image_data = BytesIO(byte_data)
                    img = Image.open(image_data)
                    img.save("cell-" + count + '.png', "PNG")
                    res.append("cell-" + count + '.png')
                # base64_data = data.sub(',', '', codec)
                # # print(stream[:10]) 
                # decodeit = open('cell-' + count + '.png', 'wb')
                # decodeit.write(base64.b64decode((stream)))
                # decodeit.close()
            else:
                res.append(output)
        return res        







if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='accept input: a jupyter notebook file')
    parser.add_argument('filename', type=str, help='pathname of jupyter notebook')
    args = parser.parse_args()

    filename = args.__getattribute__("filename")
    # print(filename)
    
    converter = JupyterCells2RO()
    converter.get_cells(filename)
    converter.buildCellsRO(filename)
