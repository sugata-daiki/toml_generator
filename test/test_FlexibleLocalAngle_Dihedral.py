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
local_ff = forcefields.make_local_forcefield_table()
flexible_local_angle = local_ff.make_FlexibleLocalAngle()

for i in range(98):
    flexible_local_angle.add_angle(i, i+1, i+2)

flexible_local_dihedral = local_ff.make_FlexibleLocalDihedral()

for i in range(97):
    flexible_local_dihedral.add_dihedral_angle(i, i+1, i+2, i+3)

toml.save_toml_file('input.toml')
