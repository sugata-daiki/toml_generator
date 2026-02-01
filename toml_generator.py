import tomlkit
from tomlkit import document, table, inline_table, aot, array, key
from tomlkit.items import Table
import constants

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

class PlatformTable:
    def __init__(self, doc):
        doc.add("platform", table())

        self.platform_table = doc["platform"]

    def set_name(self, name):
        self.platform_table["name"] = name

    def set_precision(self, precision):
        self.platform_table[key(["properties", "Precision"])] = precision

    def set_deviceIndex(self, deviceIndex):
        self.platform_table[key(["properties", "DeviceIndex"])] = deviceIndex

    def set_threads(self, threads):
        self.platform_table[key(["properties", "Threads"])] = threads

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

class ParticleParamsHandler:
    def __init__(self, params_container):
        self.params_container = params_container

    def add_particle(self, coord, residue_name, group):
        t = inline_table()

        t["m"] = constants.ATOM_MASS[residue_name]
        t["pos"] = [coord[0], coord[1], coord[2]]
        t["name"] = residue_name
        t["group"] = group

        self.params_container.append(t)

class HarmonicBondParamsHandler:
    def __init__(self, params_container, doc):
        self.params_container = params_container
        self._doc = doc

    def add_bond(self, idx1, idx2):
        systems = self._doc["systems"]
        particles = systems[0]["particles"]
        residue1 = particles[idx1]["name"]
        residue2 = particles[idx2]["name"]

        k = 110.4000
        v0 = 0.5*(constants.PARAM_EXV_SIGMA[residue1] + constants.PARAM_EXV_SIGMA[residue2])

        t = inline_table()
        t["indices"] = [idx1, idx2]
        t["k"] = k
        t["v0"] = v0
        self.params_container.append(t)

class SystemsTable:
    def __init__(self, doc):
        # [[systems]]
        if "systems" not in doc:
            doc.add("systems", aot())

        self.systems_aot = doc["systems"]

        if len(self.systems_aot) == 0:
            self.systems_aot.append(table())

        self.current_systems_table = self.systems_aot[-1]
    
    def set_boundary_shape_lower(self, coord):
        self.current_systems_table[key(["boundary_shape", "lower"])] = [coord[0], coord[1], coord[2]]

    def set_boundary_shape_upper(self, coord):
        self.current_systems_table[key(["boundary_shape", "upper"])] = [coord[0], coord[1], coord[2]]

    def set_ionic_strength(self, ionic_strength):
        self.current_systems_table[key(["attributes", "ionic_strength"])] = ionic_strength

    def set_temperature(self, temperature):
        self.current_systems_table[key(["attributes", "temperature"])] = temperature

    def make_particles_table(self):
        
        if "particles" not in self.current_systems_table:
            particles_arr = array()

        particles_arr.multiline(True)

        self.current_systems_table.add("particles", particles_arr)
        params_array = self.current_systems_table["particles"]
        return ParticleParamsHandler(params_array)

class LocalForcefieldTable:
    def __init__(self, local_aot, doc):
        self.local_aot = local_aot
        if len(self.local_aot) == 0:
            self.local_aot.append(table())

        self.current_local_table = self.local_aot[-1]
        self._doc = doc

    def make_HarmonicBond(self):
        self.current_local_table["interaction"] = "BondLength"
        self.current_local_table["potential"] = "Harmonic"
        self.current_local_table["topology"] = "bond"

        if "parameters" not in self.current_local_table:
            parameters_arr = array()

        parameters_arr.multiline(True)

        self.current_local_table.add("parameters", parameters_arr)
        params_array = self.current_local_table["parameters"]
        return HarmonicBondParamsHandler(params_array, self._doc)
        
class ForcefieldsTable:
    def __init__(self, doc):
        # [[forcefields]]
        if "forcefields" not in doc:
            doc.add("forcefields", aot())

        self.ff_aot = doc["forcefields"]

        if len(self.ff_aot) == 0:
            self.ff_aot.append(table())

        self.current_ff_table = self.ff_aot[-1]
        self._doc = doc

    def make_local_forcefield_table(self):
        # [[forcefields.local]]
        if "local" not in self.current_ff_table:
            self.current_ff_table.add("local", aot())
        return LocalForcefieldTable(self.current_ff_table["local"], self._doc)



class TOMLGenerator:
    def __init__(self):
        self._doc = document()

    def make_files_table(self):
        return FilesTable(self._doc)

    def make_platform_table(self):
        return PlatformTable(self._doc)

    def make_simulator_table(self):
        return SimulatorTable(self._doc)

    def make_systems_table(self):
        return SystemsTable(self._doc)

    def make_forcefields_table(self):
        return ForcefieldsTable(self._doc)

    def save_toml_file(self, filename):
        with open(filename, "w") as f:
            tomlkit.dump(self._doc, f)
        print(f"File saved: {filename}")

def toml():
    return TOMLGenerator()
