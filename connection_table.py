from sonata.circuit import File
import numpy as np
import pandas as pd

net = File(data_files=['network/BLA_BLA_edges.h5', 'network/BLA_nodes.h5'],
           data_type_files=['network/BLA_BLA_edge_types.csv', 'network/BLA_node_types.csv'])

print("This is gonna take a sec btw")
print('Contains nodes: {}'.format(net.has_nodes))
print('Contains edges: {}'.format(net.has_edges))


file_edges = net.edges
print('Edge populations in file: {}'.format(file_edges.population_names))
recurrent_edges = file_edges['BLA_to_BLA']

#conver_onto = 925
conver_onto = np.arange(0, 4000, 1)
#conver_onto = np.delete(conver_onto, np.where(conver_onto == 3208))
#conver_onto = np.delete(conver_onto, np.where(conver_onto == 3266))
#conver_onto = np.delete(conver_onto, np.where(conver_onto == 3390))

scale = 4
con_count = 0
PN_A_count = 0
PN_C_count = 0
PV_count = 0
SOM_count = 0
best_excit_count = 0
best_excit_cell = 0
PN_A = []
PN_C = []
SOM = []
PV = []
total_excit = []
total_inhib = []
net_excit = []
nex_excit_PV = []
label = []
for i in range(len(conver_onto)):
    PN_A_count = 0
    PN_C_count = 0
    PV_count = 0
    SOM_count = 0
    if (conver_onto[i] >= 0 and conver_onto[i] <= 568*scale+3):
        label.append('PN Type A Cell')
    if (conver_onto[i] >= 569*scale and conver_onto[i] <= 799*scale+3):
        label.append('PN Type C Cell')
    if (conver_onto[i] >= 800*scale and conver_onto[i] <= 892 * scale+3):
        label.append('PV Cell')
    if (conver_onto[i] >= 893*scale and conver_onto[i] <= 999 * scale + 4):
        label.append('SOM Cell')
    for edge in recurrent_edges.get_target(conver_onto[i]):  # we can also use get_targets([id0, id1, ...])
        assert (edge.target_node_id == conver_onto[i])
        if ((edge.source_node_id >= 0) & (edge.source_node_id <= 568 * scale)):
            PN_A_count = PN_A_count + 1
        if ((edge.source_node_id >= 569 * scale) & (edge.source_node_id <= 799 * scale)):
            PN_C_count = PN_C_count + 1
        if ((edge.source_node_id >= 800 * scale) & (edge.source_node_id <= 892 * scale)):
            PV_count = PV_count + 1
        if ((edge.source_node_id >= 893 * scale) & (edge.source_node_id <= 999 * scale + 4)):
            SOM_count = SOM_count + 1
        #print("cell %d has cell %d converging onto it" % (conver_onto, edge.source_node_id))
        con_count += 1
    PN_A.append(PN_A_count)
    PN_C.append(PN_C_count)
    SOM.append(SOM_count)
    PV.append(PV_count)
    tot_exc = PN_A_count + PN_C_count
    tot_inh = PV_count + SOM_count
    total_excit.append(tot_exc)
    total_inhib.append(tot_inh)
    net_excit.append(tot_exc - tot_inh)
    nex_excit_PV.append(tot_exc - PV_count)

print(len(label))
print(len(conver_onto))
print(len(PN_A))
d = {'cell id': conver_onto,'Cell Type':label, 'PN_A Convergence': PN_A, 'PN_C Convergence': PN_C, 'SOM Convergence': SOM,
     'PV Convergence': PV, 'Total Exc Convergence': total_excit, 'Total Inh Convergence': total_inhib,
     'Net Exc':net_excit, 'net Exc only PV': nex_excit_PV}
df = pd.DataFrame(data=d)
df.to_csv('connection table.csv')


    #print('There are {} connections onto target node #{}'.format(best_con_count, best_con_count))
    #print('There are {} PN_A connections onto target node #{}'.format(best_PN_A_count, best_excit_cell))
    #print('There are {} PN_C connections onto target node #{}'.format(best_PN_C_count, best_excit_cell))
    #print('There are {} excitatory connections onto target node #{}'.format((best_PN_A_count+best_PN_C_count), best_excit_cell))
    #print('There are {} PV connections onto target node #{}'.format(best_PV_count, best_excit_cell))
    #print('There are {} SOM connections onto target node #{}'.format(best_SOM_count, best_excit_cell))
    #print('There are {} inhibitory connections onto target node #{}'.format((best_PV_count + best_SOM_count), best_excit_cell))
    #print('There are {} net excitatory connections onto target node #{}'.format(((best_PN_A_count + best_PN_C_count) - (best_PV_count)), best_excit_cell))

