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

toml.save_toml_file('input.toml')
