import tomlkit
from tomlkit import document, table, inline_table, aot, array, key
from tomlkit.items import Table

class FilesTable:
    def __init__(self, doc):
        doc.add("files", table())

        self.files_table = doc["files"]


    def set_output_format(self, fmt):
        self.files_table[key(["output", "format"])] = fmt

    def set_output_path(self, path):
        self.files_table[key(["output", "path"])] = path

    def set_output_prefix(self, prefix):
        self.files_table[key(["output", "prefix"])] = prefix



class SimulatorTable:
    def __init__(self, doc):
        doc.add("simulator", table())

        self.simulator_table = doc["simulator"]

    def set_boundary_type(self, boundary_type):
        self.simulator_table["boundary_type"] = boundary_type

    def set_delta_t(self, delta_t):
        self.simulator_table["delta_t"] = delta_t

    def set_total_step(self, total_step):
        self.simulator_table["total_step"] = total_step

    def set_save_step(self, save_step):
        self.simulator_table["save_step"] = save_step

    def set_seed(self, seed):
        self.simulator_table["seed"] = seed

    def set_energy_minimization(self, energy_minimization):
        self.simulator_table["energy_minimization"] = energy_minimization

class TOMLGenerator:
    def __init__(self):
        self._doc = document()

    def make_files_table(self):
        return FilesTable(self._doc)

    def make_simulator_table(self):
        return SimulatorTable(self._doc)

    def save_toml_file(self, filename):
        with open(filename, "w") as f:
            tomlkit.dump(self._doc, f)
        print(f"File saved: {filename}")

def toml():
    return TOMLGenerator()
