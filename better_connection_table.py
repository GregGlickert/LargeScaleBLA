import sys

import numpy as np
import pandas as pd

from bmtools.cli.plugins.util.util import relation_matrix
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
edges = None

def conn_info(**kwargs):
    global edges
    _edges = kwargs["edges"]
    source_id_type = kwargs["sid"]
    target_id_type = kwargs["tid"]
    source_id = kwargs["source_id"]
    target_id = kwargs["target_id"]
    t_list = kwargs["target_nodes"]
    s_list = kwargs["source_nodes"]
    
    if edges is None:
        edges = _edges
    else:
        edges = edges.append(_edges).drop_duplicates()

    cons = edges[(edges[source_id_type] == source_id) & (edges[target_id_type]==target_id)]

    print(source_id)
 

def run(config):

    nodes = None
    edges = None 
    sources = ['BLA','shell']
    targets = ['BLA']
    sids = ['a_name','a_name']
    tids = ['a_name']
    prepend_pop = True
    
    print("\ttotal\tuni\tbi") 
    ret = relation_matrix(config,nodes,edges,sources,targets,sids,tids,prepend_pop,relation_func=conn_info)
    
    return

if __name__ == '__main__':
    if __file__ != sys.argv[-1]:
        run(sys.argv[-1])
    else:
        run('simulation_configECP_base_homogenous.json')

