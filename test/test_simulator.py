import numpy as np
import toml_generator as tg

toml = tg.toml()

simulator = toml.make_simulator_table()
simulator.set_boundary_type("Unlimited")
simulator.set_delta_t(0.1)
simulator.set_total_step(1000)
simulator.set_save_step(1000)
simulator.set_seed(12345)
simulator.set_energy_minimization(True)

toml.save_toml_file('input.toml')
