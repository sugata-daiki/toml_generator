import numpy as np
import toml_generator as tg

toml = tg.toml()

files = toml.make_files_table()
files.set_output_format('pdb')
files.set_output_path('path')
files.set_output_prefix('prefix')

toml.save_toml_file('input.toml')
