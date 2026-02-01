import numpy as np
import toml_generator as tg

toml = tg.toml()

files = toml.make_platform_table()
files.set_name('CUDA')
files.set_precision('single')

toml.save_toml_file('input.toml')
