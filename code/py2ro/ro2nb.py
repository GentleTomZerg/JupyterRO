import argparse
import json
from importlib_metadata import metadata
from rocrate.rocrate import ROCrate


def get_ro_cells(filename):
    ro_cells = []
    crate = ROCrate(filename)
    for e in crate.contextual_entities:
        ro_cells.append(e._jsonld)
    return ro_cells


def generate_nb(filename):
    # ro_cells = get_ro_cells(None)
    jupyter_file = JupterFile().prototype_json()
    ro_cells = get_ro_cells(filename)
    add_ro_cells(jupyter_file, ro_cells)

    with open("jupyter.ipynb", "w") as f:
        f.write(json.dumps(jupyter_file, ensure_ascii=False, indent=4))


def add_ro_cells(jupyter_file, ro_cells):
    factory = JupterFile()
    # {
    #     '@id': '#0',
    #     '@type': 'cell',
    #     'content': '@cell \ndef a():\n    print("Process a");\n',
    #     'markdown': '# This is method a\n# it prints Process a\n'
    # }
    for ro_cell in ro_cells:
        if ("markdown" in ro_cell and ro_cell["markdown"] != None):
            md_cell = factory.prototype_md_cell()
            markdown = str(ro_cell["markdown"]).replace("#", "")
            content = markdown.split("\n")
            md_cell["source"] = content
            jupyter_file["cells"].append(md_cell)
        if ("content" in ro_cell):
            code_cell = factory.prototype_code_cell()
            code_cell["source"] = ro_cell["content"]
            jupyter_file["cells"].append(code_cell)


class JupterFile:
    def __init__(self):
        pass

    def prototype_json(self):

        json = {
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3 (ipykernel)",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "codemirror_mode": {
                        "name": "ipython",
                        "version": 3
                    },
                    "file_extension": ".py",
                    "mimetype": "text/x-python",
                    "name": "python",
                    "nbconvert_exporter": "python",
                    "pygments_lexer": "ipython3",
                    "version": "3.8.10"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 5
        }
        # metadata = {}
        # kernel_info = {}
        # language_info = {}
        # metadata["kernel_info"] = kernel_info
        # metadata["language_info"] = language_info

        # json["metadata"] = metadata
        # json["nbformat"] = 4
        # json["nbformat_minor"] = 0
        json["cells"] = []

        return json

    def prototype_md_cell(self):
        cell = {
            "cell_type": "markdown",
            "metadata": {},
        }
        return cell

    def prototype_code_cell(self):
        cell = {
            "cell_type":
            "code",
            "execution_count":
            0,  # integer or null
            "metadata": {
                "collapsed":
                True,  # whether the output of the cell is collapsed
                "scrolled": False,  # any of true, false or "auto"
            },
            "outputs": []
        }

        return cell


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='accept input: a ro-crate directory')
    parser.add_argument('filename', type=str, help='pathname of ro-crate directory')
    args = parser.parse_args()

    filename = args.__getattribute__("filename")
    generate_nb(filename)