from rocrate.rocrate import ROCrate
from rocrate.model.person import Person

alice_id = "https://orcid.org/0000-0000-0000-0000"
bob_id = "https://orcid.org/0000-0000-0000-0001"


class Jupyter2RO():
    def __init__(self):
        self.crate = ROCrate()

    def buildRO(self):
        # add data entities
        jupyter_notebook = self.crate.add_file("../data/example.ipynb",
                                          properties={
                                              "name": "jupyternotebook",
                                              "encodingFormat": "application/json"
                                          })

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

        self.crate.write("../result/jupyter_crate")

    def consume(self):
        crate = ROCrate('../result/jupyter_crate')  # or ROCrate('exp_crate.zip')
        for e in crate.get_entities():
            print(e.id, e.type)




