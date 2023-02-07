from bmtk.utils.sim_setup import build_env_bionet
from bmtk.builder import NetworkBuilder
from bmtk.simulator import bionet
import os, sys
import numpy as np
import synapses
import warnings
import h5py
import synapses
import matplotlib.pyplot as plt

synapses.load()
syn = synapses.syn_params_dicts()
net = NetworkBuilder("BLA")

net.add_nodes(N=2, pop_name='PN',
              mem_potential='e',
              model_type='biophysical',
              model_template='hoc:PN_C',
              morphology=None)

#conn = net.add_edges(source={'pop_name': 'PN'}, target={'pop_name': 'PN'},
#                     iterator='one_to_one',
#                     connection_rule=1,
#                     syn_weight=1,
#                     delay=0.1,
#                     dynamics_params='PN2PN.json',
#                     model_template=syn['PN2PN.json']['level_of_detail'],
#                    distance_range=[-10000.0, 10000.0],
#                     target_sections=['soma'])

net.build()
net.save(output_dir='network')

build_env_bionet(base_dir='./',
                network_dir='./network',
                config_file='config.json',
                tstop=5000, dt=0.1,
                report_vars=['v'],
                components_dir='components',
                current_clamp={
                     'amp': 0.400,
                     'delay': 1000.0,
                     'duration': 400.0,
                     'gids': [0]
                },
                v_init=-70,
                compile_mechanisms=False,
                overwrite_config=True)