from cProfile import label
from importlib.resources import path
from re import L
import pandas as pd
from tkinter import W
import h5py
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import random
#import matplotlib.patches as mpatches
from bmtk.analyzer.compartment import plot_traces
from bmtk.utils.reports.compartment import CompartmentReport

random.seed(123412)
np.random.seed(123412)
#tone_synapses = random.sample(range(4000), 2800) # 70% of cells get a tone_synapses
#tone_synapses.sort()
#tone_synapses = random.sample(range(800,900), 40)
#print(tone_synapses)

def get_array(path):
    try:
        array = h5py.File(path,'r')
        array = (array['report']['BLA']['data'][:])
    except:
        pass
    return array


    fig, ax = plt.subplots(2,1, figsize=(12, 6),tight_layout=True)
    weight_path = "outputECP/PN2PN_W.h5"
    cai_path = "outputECP/PN2PN_cai.h5"
    weight_array = get_array(weight_path)
    cai_array = get_array(cai_path)
    cai_array[:] = [x * 1000 for x in cai_array] #to fix units
    ax[0].plot(weight_array)
    ax[1].plot(cai_array)
    plt.suptitle("PN2PN")
    plt.show()

def check_distro(path,endtime):
    fig, ax = plt.subplots(1,2, figsize=(12, 6),tight_layout=True,sharey=True)
    W = get_array(path=path)
    weight_at_start = []
    weight_at_end = []
    for i in range(len(W[0])):
        weight_at_start.append(W[0][i])
    for i in range(len(W[0])):
        weight_at_end.append(W[(endtime*10)-1][i])
    ax[0].hist(weight_at_start, bins=30)
    ax[0].set_title('syn_weight at time 0')
    ax[0].set_ylabel('# of synapses')
    ax[0].set_xlabel('syn_weight')
    ax[1].hist(weight_at_end, bins=30)
    ax[1].set_xlabel('syn_weight')
    ax[1].set_title("syn weight at 10000ms")
    plt.suptitle(path)
    plt.show()

def compare_weight(array, start_time, end_time, decay_over_10sec = 0.0046369585134881175, decay_weight=30,fudge_factor = 80):
    W = array
    weight_at_start = []
    weight_at_end = []

    for i in range(len(W)):
        weight_at_start.append(W[i][:(start_time*10)+1])
    for i in range(len(W)):
        weight_at_end.append(W[i][(end_time*10)-1:])
    lower_than_start_weight = 0
    higher_than_start_weight = 0
    decay_weight = 0
    for i in range(len(weight_at_start)):
        if ((weight_at_start[i] - weight_at_end[i]) * (decay_weight/weight_at_start[i]) < decay_over_10sec * fudge_factor
        and weight_at_start > weight_at_end):
            decay_weight = decay_weight + 1
        if ((weight_at_start[i] - weight_at_end[i]) * (decay_weight/weight_at_start[i]) > decay_over_10sec * fudge_factor
        and weight_at_start > weight_at_end):
            lower_than_start_weight = lower_than_start_weight + 1
        if ((weight_at_start[i] - weight_at_end[i]) * (decay_weight/weight_at_start[i]) > decay_over_10sec * fudge_factor
        and weight_at_start < weight_at_end):
            higher_than_start_weight = higher_than_start_weight + 1
    #print(weight_at_start[0] - weight_at_end[0])

    precent_higher = higher_than_start_weight/len(weight_at_start)*100
    precent_lower = lower_than_start_weight/len(weight_at_start)*100
    precent_decay = decay_weight/(len(weight_at_start))*100
    print("data for {}".format(path))
    print("Number of synapses that decayed {} {:.2f}%".format(decay_weight,precent_decay))
    print("Number of synpases that entered LTP {} {:.2f}%".format(higher_than_start_weight,precent_higher))
    print("Number of synpases that entered LTD {} {:.2f}%".format(lower_than_start_weight,precent_lower))
    print("\n")

def compare_weight_old(path, start_time, end_time, decay_over_10sec = 0.0005, decay_weight=30,fudge_factor = 4):
    W = get_array(path=path)
    weight_at_start = []
    weight_at_end = []
    for i in range(len(W[0])):
        weight_at_start.append(W[start_time*10][i])
    for i in range(len(W[0])):
        weight_at_end.append(W[(end_time*10)-1][i])
    lower_than_start_weight = 0
    higher_than_start_weight = 0
    decay_weight = 0
    for i in range(len(weight_at_start)):
        if ((weight_at_start[i] - weight_at_end[i]) * (decay_weight/weight_at_start[i]) < decay_over_10sec * fudge_factor
        and weight_at_start[i] > weight_at_end[i]):
            decay_weight = decay_weight + 1
        if ((weight_at_start[i] - weight_at_end[i]) * (decay_weight/weight_at_start[i]) > decay_over_10sec * fudge_factor
        and weight_at_start[i] > weight_at_end[i]):
            lower_than_start_weight = lower_than_start_weight + 1
            #print(weight_at_start[i],weight_at_end[i])
        if ((weight_at_start[i] - weight_at_end[i]) * (decay_weight/weight_at_start[i]) > decay_over_10sec * fudge_factor
        and weight_at_start[i] < weight_at_end[i]):
            higher_than_start_weight = higher_than_start_weight + 1

    precent_higher = higher_than_start_weight/len(weight_at_start)*100
    precent_lower = lower_than_start_weight/len(weight_at_start)*100
    precent_decay = decay_weight/(len(weight_at_start))*100
    print("data for {}".format(path))
    print("Number of synapses that decayed {} {:.2f}%".format(decay_weight,precent_decay))
    print("Number of synpases that entered LTP {} {:.2f}%".format(higher_than_start_weight,precent_higher))
    print("Number of synpases that entered LTD {} {:.2f}%".format(lower_than_start_weight,precent_lower))
    print("\n")

def get_gids_and_data_arrays_plus_hib(path):
    file = h5py.File(path, 'r')
    cai_trace = file['report']['BLA']['data']

    time_ds = file['report/BLA/mapping/time']
    tstart = time_ds[0]
    tstop = time_ds[1]
    #x_axis = np.linspace(tstart, tstop, len(cai_trace), endpoint=True)

    gids_ds = file['report/BLA/mapping/node_ids']
    index_ds = file['report/BLA/mapping/index_pointer']
    gids_ds = [0,1,2,3,4,5,6,7,8,10]
    index_lookup = {gids_ds[i]: (index_ds[i], index_ds[i+1]) for i in range(len(gids_ds))}
    tone_noise_data = []
    tone_trial_data = []
    #print(gids_ds[:])
    for i in tqdm(range(len(gids_ds))):
        if(gids_ds[i] in tone_synapses):
            var_indx = index_lookup[gids_ds[i]][0]
            data = cai_trace[:,var_indx]
            tone_trial_data.append(data)
        else:
            var_indx = index_lookup[gids_ds[i]][0]
            data = cai_trace[:,var_indx]
            tone_noise_data.append(data)
    print("tone trial")
    compare_weight(tone_trial_data,start_time = 0,end_time=10000)
    print('tone noise')
    compare_weight(tone_noise_data,start_time = 0,end_time=10000)

def potential(pot_path,depress_path):
    print(pot_path,depress_path)
    report_pot = CompartmentReport(pot_path)
    #report_dep = CompartmentReport(depress_path)
    array = report_pot.data()
    potent_count = 0
    depressing_count = 0
    both_count = 0
    cells = report_pot.node_ids()
    for i in tqdm(range(len(report_pot.node_ids()))):
        data_pot = report_pot.data(node_id=i)
        #data_dep = report_dep.data(node_id=i)
        if 1 in data_pot: # 1 means the flag was set to pot or depress at some point in the run
            both_count = both_count + 1
        #if 1 in data_dep and not 1 in data_pot:
        #    depressing_count = depressing_count + 1
        #if 1 in data_pot and not 1 in data_dep:
        #    potent_count = potent_count + 1
    print("{} synapses did only LTD".format(depressing_count))
    print("{} synapses did only LTP".format(potent_count))
    print("{} synapses did both LTP and LTD".format(both_count))

#potential(pot_path="outputECP/tone2PN_pot_flag.h5", depress_path="outputECP/tone2PN_dep_flag.h5")
def plot_tone2PN():
    fig, axs = plt.subplots(2, 2, figsize=(18, 6))
    tone2PN = get_array('outputECP/tone2PN_cai.h5')
    axs[0][0].plot(tone2PN)
    axs[0][0].set_title("Cai")

    tone2PN = get_array('outputECP/tone2PN_rho.h5')
    axs[1][0].plot(tone2PN)
    axs[1][0].set_title("Rho")

    tone2PN = get_array('outputECP/tone2PN.h5')
    axs[0][1].plot(tone2PN)
    axs[0][1].set_title("weight")

    tone2PN = get_array('outputECP/tone2PN_pot_flag.h5')
    LTP = axs[1][1].plot(tone2PN,'r')
    tone2PN = get_array('outputECP/tone2PN_dep_flag.h5')
    LTD = axs[1][1].plot(tone2PN,'b')
    axs[1][1].set_title("LTD/LTP flags")
   
    fig.suptitle("tone2PN")
    plt.show()

def plot_tone2PV():
    fig, axs = plt.subplots(2, 2, figsize=(18, 6))
    tone2PV = get_array('outputECP/tone2PV_cai.h5')
    axs[0][0].plot(tone2PV)
    axs[0][0].set_title("Cai")

    tone2PV = get_array('outputECP/tone2PV_rho.h5')
    axs[1][0].plot(tone2PV)
    axs[1][0].set_title("Rho")

    tone2PV = get_array('outputECP/tone2PV.h5')
    axs[0][1].plot(tone2PV)
    axs[0][1].set_title("weight")

    tone2PV = get_array('outputECP/tone2PV_pot_flag.h5')
    LTP = axs[1][1].plot(tone2PV,'r')
    tone2PV = get_array('outputECP/tone2PV_dep_flag.h5')
    LTD = axs[1][1].plot(tone2PV,'b')
    axs[1][1].set_title("LTD/LTP flags")
   
    fig.suptitle("tone2PV")
    plt.show()

def plot_PN2PV():
    fig, axs = plt.subplots(2, 2, figsize=(18, 6))
    PN2PV = get_array('outputECP/PN2PV_cai.h5')
    axs[0][0].plot(PN2PV)
    axs[0][0].set_title("Cai")

    PN2PV = get_array('outputECP/PN2PV_rho.h5')
    axs[1][0].plot(PN2PV)
    axs[1][0].set_title("Rho")

    PN2PV = get_array('outputECP/PN2PV.h5')
    axs[0][1].plot(PN2PV)
    axs[0][1].set_title("weight")

    PN2PV = get_array('outputECP/PN2PV_pot_flag.h5')
    LTP = axs[1][1].plot(PN2PV,'r')
    PN2PV = get_array('outputECP/PN2PV_dep_flag.h5')
    LTD = axs[1][1].plot(PN2PV,'b')
    axs[1][1].set_title("LTD/LTP flags")
   
    fig.suptitle("PN2PV")
    plt.show()

#plot_tone2PN()
#print("\ndoing tone2PN baseline\n")
#potential(pot_path="outputECP/tone2PN_pot_flag.h5",depress_path="outputECP/tone2PN_dep_flag.h5")
#print("\nDoing tone to PV  baseline now\n")
#potential(pot_path="outputECP/tone2PV_pot_flag.h5",depress_path="outputECP/tone2PV_dep_flag.h5")
print("\ndoing tone2PN trials now\n")
potential(pot_path="output_trials_tone_only/tone2PN_pot_flag.h5",depress_path="output_trials_tone_only/tone2PN_dep_flag.h5")
#print("\nDoing tone to PV trials now\n")
#potential(pot_path="outputECP_trials/tone2PV_pot_flag.h5",depress_path="outputECP_trials/tone2PV_dep_flag.h5")
#plot_tone2PV()
#plot_PN2PV()

#outputECP/tone2PN_pot_flag.h5 outputECP/tone2PN_dep_flag.h5
#72 synapses did only LTD
#0 synapses did only LTP
#0 synapses did both LTP and LTD
#outputECP/tone2PN trials
#2488 synapses did only LTD
# synapses did only LTP
#5 synapses did both LTP and LTD