from sonata.circuit import File
import numpy as np

net = File(data_files=['network/BLA_BLA_edges.h5', 'network/BLA_nodes.h5'],
           data_type_files=['network/BLA_BLA_edge_types.csv', 'network/BLA_node_types.csv'])


print('Contains nodes: {}'.format(net.has_nodes))
print('Contains edges: {}'.format(net.has_edges))


file_edges = net.edges
print('Edge populations in file: {}'.format(file_edges.population_names))
recurrent_edges = file_edges['BLA_to_BLA']

#conver_onto = 925
conver_onto = np.arange(3200, 3568, 1)
conver_onto = np.delete(conver_onto, np.where(conver_onto == 3208))
conver_onto = np.delete(conver_onto, np.where(conver_onto == 3266))
conver_onto = np.delete(conver_onto, np.where(conver_onto == 3390))

scale = 4
con_count = 0
PN_A_count = 0
PN_C_count = 0
PV_count = 0
SOM_count = 0
best_excit_count = 0
best_excit_cell = 0
for i in range(len(conver_onto)):
    PN_A_count = 0
    PN_C_count = 0
    PV_count = 0
    SOM_count = 0
    for edge in recurrent_edges.get_target(conver_onto[i]):  # we can also use get_targets([id0, id1, ...])
        assert (edge.target_node_id == conver_onto[i])
        if ((edge.source_node_id >= 0) & (edge.source_node_id <= 568 * scale)):
            PN_A_count = PN_A_count + 1
        if ((edge.source_node_id >= 569 * scale) & (edge.source_node_id <= 799 * scale)):
            PN_C_count = PN_C_count + 1
        if ((edge.source_node_id >= 800 * scale) & (edge.source_node_id <= 892 * scale)):
            PV_count = PV_count + 1
        if ((edge.source_node_id >= 893 * scale) & (edge.source_node_id <= 999 * scale)):
            SOM_count = SOM_count + 1
        #print("cell %d has cell %d converging onto it" % (conver_onto, edge.source_node_id))
        con_count += 1
    total_excit = PN_A_count + PN_C_count
    total_inhib = PV_count
    net_excit = total_excit - total_inhib
    if (net_excit > best_excit_count):
        best_excit_count = net_excit
        best_PN_A_count = PN_A_count
        best_PN_C_count = PN_C_count
        best_PV_count = PV_count
        best_SOM_count = SOM_count
        best_excit_cell = conver_onto[i]
        best_con_count = con_count

print('There are {} connections onto target node #{}'.format(best_con_count, best_con_count))
print('There are {} PN_A connections onto target node #{}'.format(best_PN_A_count, best_excit_cell))
print('There are {} PN_C connections onto target node #{}'.format(best_PN_C_count, best_excit_cell))
print('There are {} excitatory connections onto target node #{}'.format((best_PN_A_count+best_PN_C_count), best_excit_cell))
print('There are {} PV connections onto target node #{}'.format(best_PV_count, best_excit_cell))
print('There are {} SOM connections onto target node #{}'.format(best_SOM_count, best_excit_cell))
print('There are {} inhibitory connections onto target node #{}'.format((best_PV_count + best_SOM_count), best_excit_cell))
print('There are {} net excitatory connections onto target node #{}'.format(((best_PN_A_count + best_PN_C_count) - (best_PV_count)), best_excit_cell))

