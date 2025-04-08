import os, sys
from bmtk.simulator import bionet
import numpy as np
import synapses
import warnings
import json
import pathlib
from bmtk.simulator.bionet.pyfunction_cache import add_weight_function
from neuron import h

import argparse

CONFIG = 'config.json'
USE_CORENEURON = False

def get_synaptic_params(path_to_syn_folder):
    """Gets values of all json files and puts them into one file"""
    combined_data = []
    # List all files in the input folder
    for filename in os.listdir(path_to_syn_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(path_to_syn_folder, filename)
            
            # Open and read the JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)
                # Append the filename and its data
                combined_data.append({
                    'filename': filename,
                    'data': data
                })
    return combined_data

def save_synaptic_params(data,path_to_output_dir):
    """Saves combined json data into one file"""
    with open(path_to_output_dir, 'w') as output_file:
        json.dump(data, output_file, indent=4)


def run(config_file=CONFIG, use_coreneuron=USE_CORENEURON):
    warnings.simplefilter(action='ignore', category=FutureWarning)

    synapses.load()
    

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
    
    
    
    with open(config_file, 'r') as json_file:
        conf_dict = json.load(json_file)
        if os.environ.get("OUTPUT_DIR"):
            output_dir = os.path.abspath(os.environ.get('OUTPUT_DIR'))
            pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
            conf_dict['manifest']['$OUTPUT_DIR'] = output_dir
            synaptic_report_dir = output_dir + "/synaptic_report.json"
            syn_data = get_synaptic_params('components/synaptic_models')

    # # register synaptic weight function
    # synapses.load(randseed=1111)
    # add_weight_function(synapses.lognormal_weight, name='lognormal_weight')

    if use_coreneuron:
        import corebmtk
        conf = corebmtk.Config.from_json(conf_dict, validate=True)
    else:
        conf = bionet.Config.from_json(conf_dict, validate=True)

    conf.build_env()
    graph = bionet.BioNetwork.from_config(conf)
    
    # This fixes the morphology error in LFP calculation
    pop = graph._node_populations['BLA']
    for node in pop.get_nodes():
        node._node._node_type_props['morphology'] = node.model_template[1]

    if use_coreneuron:
        sim = corebmtk.CoreBioSimulator.from_config(
            conf, network=graph, gpu=False)
    else:
        sim = bionet.BioSimulator.from_config(conf, network=graph)

    '''
    # This calls insert_mechs() on each cell to use its gid as a seed
    # to the random number generator, so that each cell gets a different
    # random seed for the point-conductance noise
    cells = graph.get_local_cells()
    for cell in cells:
        cells[cell].hobj.insert_mechs(cells[cell].gid)
    '''
    cells = graph.get_local_cells()
    for cell in cells:
        cells[cell].hobj.insert_mechs(cells[cell].gid)
        
    # Setup ACh
    # add a line to config 
    #   "ACH_level": 0, 1, 2
    # to start executing this
    if conf.get('ACH_level'):
        # 1. Get the list of cells that have been pre-selected as ACH receptive
        # from the node_sets.json file
        ach_receptive_cells = conf['node_sets'].get('ach_cells')
        print(f"{len(ach_receptive_cells)} cells are set to be receptive to ACH")

        # 2. Iterate through each cell in the network and if it's receptive, alter the synapse
        total_modified_synapses = 0
        num_modified_synapses = 0
        ach_receptive_property = "ACH"
        ach_recpetive_property_on_value = conf.get("ACH_level", 1) #default no ACH delivered
        for cell_id, cell in graph._rank_node_ids['BLA'].items():
            if cell_id in ach_receptive_cells:
                cell_connections = cell.connections()
                for connection in cell_connections:
                    syn = connection._syn
                    if hasattr(syn, ach_receptive_property):
                        setattr(syn, ach_receptive_property, ach_recpetive_property_on_value)
                        num_modified_synapses += 1
                total_modified_synapses += len(cell_connections)

        print(f"ACH turned on for {len(ach_receptive_cells)} muscarinic (synaptic) receptors")
        print(f"{num_modified_synapses}/{total_modified_synapses} ACH synapses modified")
        print(f"{ach_receptive_property} set to value {ach_recpetive_property_on_value}")
        
        # 3. Turn on nicotinic receptors per cell
        nic_cells_turned_on = 0
        for cell in ach_receptive_cells:
            hobj = cells[cell].hobj
            if hasattr(hobj, 'activate_ach'):
                hobj.activate_ach()
                nic_cells_turned_on += 1
        print(f"{nic_cells_turned_on}/{len(ach_receptive_cells)} nicotinic (intrinsic) receptors turned on")

    # clear ecp temporary directory to avoid errors
    pc = h.ParallelContext()
    if pc.id() == 0:
        try:
            ecp_tmp = conf['reports']['ecp']['tmp_dir']
        except:
            pass
        else:
            if os.path.isdir(ecp_tmp):
                for f in os.listdir(ecp_tmp):
                    if f.endswith(".h5"):
                        try:
                            os.remove(os.path.join(ecp_tmp, f))
                        except Exception as e:
                            print(f'Failed to delete {f}. {e}')
    pc.barrier()


    sim.run()
    # must be ran after sim.run since that creates dir
    if pc.id() == 0:
        save_synaptic_params(syn_data,synaptic_report_dir)
    bionet.nrn.quit_execution()
    
if __name__ == '__main__':
    for i, s in enumerate(sys.argv):
        if s in __file__:
            break

    if i < len(sys.argv) - 1:
        argv = sys.argv[i + 1:]
        for i in range(1, len(argv)):
            argv[i] = eval(argv[i])
        run(*argv)
    else:
        run()
