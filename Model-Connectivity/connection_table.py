from sonata.circuit import File
import numpy as np
import pandas as pd
from tqdm import tqdm
import random

random.seed(123412)
np.random.seed(123412)


net = File(data_files=['network_homogenous_1000/BLA_BLA_edges.h5', 'network_homogenous_1000/BLA_nodes.h5'],
           data_type_files=['network_homogenous_1000/BLA_BLA_edge_types.csv', 'network_homogenous_1000/BLA_node_types.csv'])

print('Contains nodes: {}'.format(net.has_nodes))
print('Contains edges: {}'.format(net.has_edges))

file_edges = net.edges
print('Edge populations in file: {}'.format(file_edges.population_names))
recurrent_edges = file_edges['BLA_to_BLA']


#conver_onto = [1,2,3,4,5,6,7,8,9,10]
conver_onto = np.arange(1,944, 1)
winner_cells = [137, 142, 502, 575, 577, 580, 582, 585, 588, 596, 597, 598, 600, 601, 603, 605, 606, 616, 622, 629, 633, 637, 654, 656, 664, 672, 675, 679, 684, 685, 689, 690, 694, 696, 699, 704, 706, 708, 709, 712, 714, 716, 720, 722, 728, 731, 736, 738, 740, 743, 745, 746, 748, 753, 760, 761, 763, 767, 772, 773, 776, 777, 782, 789, 791]




scale = 1
cell_count = scale * 1000
tone_synapses = random.sample(range(cell_count), int(cell_count*0.7))
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
WINNERS = []
PV_WINNER_CONS = []
PV_WINNER_CONS_count = 0
label_winner = []
label_tone_trial_synapse = []
total_excit = []
total_inhib = []
net_excit = []
nex_excit_PV = []
total_conns = []
label = []

disynapses = [0] * len(conver_onto)

def easy_table():
    print("Generating connection table")
    for i in tqdm(range(len(conver_onto))):
        PN_A_count = 0
        PN_C_count = 0
        PV_count = 0
        SOM_count = 0
        con_count = 0
        PV_WINNER_CONS_count = 0
        winner_count = 0
        if (conver_onto[i] >= 0 and conver_onto[i] <= 568):
            label.append('PN Type A Cell')
        if (conver_onto[i] >= 569 and conver_onto[i] <= 799):
            label.append('PN Type C Cell')
        if (conver_onto[i] >= 800 and conver_onto[i] <= 893):
            label.append('PV Cell')
        if (conver_onto[i] >= 894 and conver_onto[i] <= 944):
            label.append('SOM Cell')
        if conver_onto[i] in winner_cells:
            label_winner.append('Winner')
        else:
            label_winner.append('Loser')
        if conver_onto[i] in tone_synapses and conver_onto[i] < 893:
            label_tone_trial_synapse.append("recieves tone")
        else:
            label_tone_trial_synapse.append("does not recieve tone")
        


        # check what cell connects to cover cell(target cell)
        for edge in recurrent_edges.get_target(conver_onto[i]):  # we can also use get_targets([id0, id1, ...])
            #assert (edge.target_node_id == conver_onto[i])
            if ((edge.source_node_id >= 0) & (edge.source_node_id < (568 * scale)+scale)):
                PN_A_count = PN_A_count + 1
            if ((edge.source_node_id >= 569 * scale) & (edge.source_node_id < (799 * scale)+scale)):
                PN_C_count = PN_C_count + 1
            if ((edge.source_node_id >= 800 * scale) & (edge.source_node_id < (893 * scale)+scale)):
                PV_count = PV_count + 1
            if ((edge.source_node_id >= 893 * scale) & (edge.source_node_id < (944 * scale)+scale)):
                SOM_count = SOM_count + 1
            if edge.source_node_id in winner_cells:
                winner_count = winner_count + 1
            if (conver_onto[i] >= 800 and conver_onto[i] <= 893):
                if ((edge.source_node_id >= 0) & (edge.source_node_id < (799 * scale)+scale)):
                    if edge.source_node_id in winner_cells:
                        PV_WINNER_CONS_count = PV_WINNER_CONS_count + 1
            con_count += 1
        
        if (conver_onto[i] >= 800 and conver_onto[i] <= 893):
            for n in range(800):    
                for edge in recurrent_edges.get_target(n):
                    if (edge.source_node_id == conver_onto[i]):
                        current_disyn_count = disynapses[n]
                        current_disyn_count = current_disyn_count + PV_WINNER_CONS_count
                        disynapses[n] = current_disyn_count

                

            
        
        PN_A.append(PN_A_count)
        PN_C.append(PN_C_count)
        SOM.append(SOM_count)
        PV.append(PV_count)
        WINNERS.append(winner_count)
        tot_exc = PN_A_count + PN_C_count
        tot_inh = PV_count + SOM_count
        total_excit.append(tot_exc)
        total_inhib.append(tot_inh)
        net_excit.append(tot_exc - tot_inh)
        nex_excit_PV.append(tot_exc - PV_count)
        total_conns.append(PN_A_count+PN_C_count+PV_count+SOM_count)



    d = {'cell id': conver_onto,'Cell Type':label, 'PN_A Convergence': PN_A, 'PN_C Convergence': PN_C, 'SOM Convergence': SOM,
         'PV Convergence': PV, 'Total Exc Convergence': total_excit, 'Total Inh Convergence': total_inhib,
         'Net Exc':net_excit, 'net Exc only PV': nex_excit_PV, 'Total number of connections': total_conns,
         'Winner connections': WINNERS,'is winner?':label_winner,'recieves tone?': label_tone_trial_synapse,
         'disynapses': disynapses}
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

def bi_connections():
    print("finding bi conns")
    # Loops over every cell and gets every connection made in the network
    for i in tqdm(range(len(conver_onto))):
        for edge in recurrent_edges.get_target(conver_onto[i]):
            assert (edge.target_node_id == conver_onto[i])
            source = edge.source_node_id
            target = edge.target_node_id
            s.append(source)
            t.append(target)
    print("Few more things to do be done in a second")
    df = pd.DataFrame({'Source': s, 'Target': t})
    df_flip = pd.DataFrame({'Source': t, "Target": s})
    df_bi = df.append(df_flip)
    # if after flipping the array there is a duplicate that means there is a bi conn
    df_bi = df_bi[df_bi.duplicated()]

    PN_PN_bi = []
    PN_PV_bi = []
    PN_SOM_bi = []
    PV_PV_bi = []

    PN2PN_count_bi = 0
    PN2PV_count_bi = 0
    PN2SOM_count_bi = 0
    PV2PV_count_bi = 0

    PN2PN_count = 0
    PN2PV_count = 0
    PV2PN_count = 0
    PN2SOM_count = 0
    PV2PV_count = 0
    SOM2PN_count = 0

    #print(df_bi)
    # out of all the bi cons
    for i in (range(len(df_bi))):
        if ((df_bi['Source'].values[i] <= (799*scale+3)) and (df_bi['Target'].values[i] <= (799*scale+3))):
            PN2PN_count_bi = PN2PN_count_bi + 1
            #PN_PN_bi.append((df_bi['Source'].values[i], df_bi['Target'].values[i]))
            #print(PN_PN_bi)
        elif ((df_bi['Source'].values[i] <= (799 * scale + 3)) and (df_bi['Target'].values[i] >= (800 * scale)) and (df_bi['Target'].values[i] <= (892*scale+3))):
            PN2PV_count_bi = PN2PV_count_bi + 1
            #PN_PV_bi.append((df_bi['Source'].values[i], df_bi['Target'].values[i]))
        elif ((df_bi['Source'].values[i] <= (799 * scale + 3)) and (df_bi['Target'].values[i] >= (893 * scale))):
            PN2SOM_count_bi = PN2SOM_count_bi + 1
            #PN_SOM_bi.append((df_bi['Source'].values[i], df_bi['Target'].values[i]))
        elif ((df_bi['Source'].values[i] >= (800 * scale)) and (df_bi['Source'].values[i] <= (892 * scale + 3)) and (df_bi['Target'].values[i] >= (800 * scale))
             and (df_bi['Target'].values[i] <= (892 * scale + 3))):
            PV2PV_count_bi = PV2PV_count_bi + 1
            #PV_PV_bi.append((df_bi['Source'].values[i], df_bi['Target'].values[i]))
        #else:
            #print(df_bi['Source'].values[i], df_bi['Target'].values[i])

    for i in (range(len(df))):
        if df['Source'].values[i] <= 799*scale+3 and df['Target'].values[i] <= 799*scale+3:
            PN2PN_count = PN2PN_count + 1
        elif df['Source'].values[i] <= 799 * scale + 3 and df['Target'].values[i] >= 800 * scale and df['Target'].values[i] <= 892*scale+3:
            PN2PV_count = PN2PV_count + 1
        elif df['Target'].values[i] <= 799 * scale + 3 and df['Source'].values[i] >= 800 * scale and df['Source'].values[i] <= 892 * scale + 3:
            PV2PN_count = PV2PN_count + 1
        elif df['Source'].values[i] <= 799 * scale + 3 and df['Target'].values[i] >= 893 * scale:
            PN2SOM_count = PN2SOM_count + 1
        elif df['Target'].values[i] <= 799 * scale + 3 and df['Source'].values[i] >= 893 * scale:
            SOM2PN_count = SOM2PN_count + 1
        elif ((df['Source'].values[i] >= (800 * scale)) and (df['Source'].values[i] <= (892 * scale + 3)) and (df['Target'].values[i] >= (800 * scale))
              and (df['Target'].values[i] <= (892 * scale + 3))):
            PV2PV_count = PV2PV_count + 1


    #print("Out of all the PN2PN connections {}% are bi connections".format(round(PN2PN_count_bi/PN2PN_count,3)))
    #print(PN2SOM_count_bi)
    #rint(PN2PN_count_bi)
    #rint(PN2PV_count_bi)
    #print(PV2PV_count_bi)
    #print(len(df_bi))
    #df_bi.to_csv('bi conns.csv')
    print("Out of all the PN2PN connections {}% are bi connections".format(round((PN2PN_count_bi/PN2PN_count)*100,3)))
    print("Out of all the PN2PV connections {}% are bi connections".format(round((PN2PV_count_bi/PN2PV_count)*100,3)))
    print("Out of all the PV2PN connections {}% are bi connections".format(round((PN2PV_count_bi/PV2PN_count)*100,3)))
    print("Out of all the PV2PV connections {}% are bi connections".format(round((PV2PV_count_bi/PV2PV_count)*100,3)))
    print("Out of all the PN2SOM connections {}% are bi connections".format(round((PN2SOM_count_bi/PN2SOM_count)*100,3)))
    print("Out of all the SOM2PN connections {}% are bi connections".format(round((PN2SOM_count_bi/SOM2PN_count)*100,3)))
    print(PN2PN_count_bi, PN2PV_count_bi, PN2SOM_count_bi, PV2PV_count_bi)
    print(PN2PN_count, PN2PV_count, PV2PN_count, PN2SOM_count, SOM2PN_count, PV2PV_count)
    #df_bi = pd.DataFrame({"PN2PN bi connections":PN_PN_bi, "PN2PV bi connections": PN_PV_bi, "PV2PV bi connections":PV_PV_bi, "PN2SOM bi connection":PN_SOM_bi})
    #print(df_bi)

easy_table()

#bi_connections()


