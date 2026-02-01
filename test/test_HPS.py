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
global_ff = forcefields.make_global_forcefield_table()

lj_attr = global_ff.make_LennardJonesAttractive()
lj_attr.add_LennardJonesAttractive_params()

lj_rep = global_ff.make_LennardJonesRepulsive()
lj_rep.add_LennardJonesRepulsive_params()

dh = global_ff.make_DebyeHuckel()
dh.add_DebyeHuckel_params()

toml.save_toml_file('input.toml')
