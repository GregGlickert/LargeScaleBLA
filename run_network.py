import os, sys
from bmtk.simulator import bionet
import numpy as np
import synapses
import warnings
import corebmtk
from neuron import coreneuron
from neuron import h
import reports


def run(config_file):
    pc = h.ParallelContext()
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=UserWarning)
    synapses.load()
    from bmtk.simulator.bionet.pyfunction_cache import add_weight_function

    def gaussianBL(edge_props, source, target):
        w0 = edge_props["syn_weight"]
        sigma = edge_props["weight_sigma"]
        return np.random.normal(w0, sigma, 1)
	
    def lognormal(edge_props, source, target):
        m = edge_props["syn_weight"]
        s = edge_props["weight_sigma"]
        mean = np.log(m) - 0.5 * np.log((s/m)**2+1)
        std = np.sqrt(np.log((s/m)**2 + 1))
        return np.random.lognormal(mean, std, 1)

    add_weight_function(lognormal)
    add_weight_function(gaussianBL)


    #conf = bionet.Config.from_json(config_file, validate=True)
    conf = corebmtk.Config.from_json(config_file, validate=True)
    conf.build_env()

    graph = bionet.BioNetwork.from_config(conf)

    # This fixes the morphology error in LFP calculation
    pop = graph._node_populations['BLA']
    for node in pop.get_nodes():
        node._node._node_type_props['morphology'] = node.model_template[1]

    sim = corebmtk.CoreBioSimulator.from_config(conf, network=graph,gpu=False)
    #sim = bionet.BioSimulator.from_config(conf, network=graph)
    
    # This calls insert_mechs() on each cell to use its gid as a seed
    # to the random number generator, so that each cell gets a different
    # random seed for the point-conductance noise
    cells = graph.get_local_cells()
    for cell in cells:
        #print(cells[cell].gid)
        cells[cell].hobj.insert_mechs((cells[cell].gid))
        pass
    
    voltage_gids = [0,1,2,3,4,5]
    reports.voltage_record(voltage_gids)
    sim.run()
    reports.save_voltage()
    bionet.nrn.quit_execution()


if __name__ == '__main__':
    if __file__ != sys.argv[-1]:
        run(sys.argv[-1])
    else:
        run('simulation_config_spikes_only.json')
