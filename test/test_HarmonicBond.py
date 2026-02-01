import numpy as np
import toml_generator as tg

toml = tg.toml()

systems = toml.make_systems_table()
systems.set_boundary_shape_lower(np.zeros(3))
systems.set_boundary_shape_upper(np.zeros(3))
systems.set_ionic_strength(0.15)
systems.set_temperature(300.0)

particles = systems.make_particles_table()

for i in range(100):
    particles.add_particle(np.zeros(3), "ALA", "dummy")

forcefields = toml.make_forcefields_table()
HarmonicBond = forcefields.make_local_forcefield_table()
hb_params = HarmonicBond.make_HarmonicBond()

for i in range(99):
    hb_params.add_bond(i, i+1)

toml.save_toml_file('input.toml')
