from importlib.resources import path
from re import L
from tkinter import W
import h5py
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.patches as mpatches
from bmtk.analyzer.compartment import plot_traces



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

def plot_PN2PV():
    fig, ax = plt.subplots(2,1, figsize=(12, 6),tight_layout=True)
    weight_path = "outputECP/PN2PV_W.h5"
    cai_path = "outputECP/PN2PV_cai.h5"
    weight_array = get_array(weight_path)
    cai_array = get_array(cai_path)
    cai_array[:] = [x * 1000 for x in cai_array] #to fix units
    ax[0].plot(weight_array)
    ax[1].plot(cai_array)
    plt.suptitle("PN2PV")
    plt.show()

def plot_tone2pyr():
    fig, ax = plt.subplots(2,1, figsize=(12, 6),tight_layout=True)
    weight_path = "outputECP/tone2PN_W.h5"
    cai_path = "outputECP/tone2PN_cai.h5"
    weight_array = get_array(weight_path)
    cai_array = get_array(cai_path)
    cai_array[:] = [x * 1000 for x in cai_array] #to fix units
    ax[0].plot(weight_array)
    ax[1].plot(cai_array)
    plt.suptitle("tone2pyr")
    plt.savefig("test.png")

def plot_tone2pyr_noise():
    fig, ax = plt.subplots(2,1, figsize=(12, 6),tight_layout=True)
    weight_path = "outputECP/bg_tone2PN_W.h5"
    cai_path = "outputECP/bg_tone2PN_cai.h5"
    weight_array = get_array(weight_path)
    cai_array = get_array(cai_path)
    cai_array[:] = [x * 1000 for x in cai_array] #to fix units
    ax[0].plot(weight_array)
    ax[1].plot(cai_array)
    plt.suptitle("tone2pyr noise")
    plt.show()

def plotPV2PN():
    fig, ax = plt.subplots(2,1, figsize=(12, 6),tight_layout=True)
    weight_path = "outputECP/PV2PN_W.h5"
    cai_path = "outputECP/PV2PN_cai.h5"
    weight_array = get_array(weight_path)
    cai_array = get_array(cai_path)
    cai_array[:] = [x * 1000 for x in cai_array] #to fix units
    ax[0].plot(weight_array)
    ax[1].plot(cai_array)
    plt.suptitle("PV2PN")
    plt.show()

def plotTone2PV():
    fig, ax = plt.subplots(2,1, figsize=(12, 6),tight_layout=True)
    weight_path = "outputECP/tone2PV_W.h5"
    cai_path = "outputECP/tone2PV_cai.h5"
    weight_array = get_array(weight_path)
    cai_array = get_array(cai_path)
    cai_array[:] = [x * 1000 for x in cai_array] #to fix units
    ax[0].plot(weight_array)
    ax[1].plot(cai_array)
    plt.suptitle("PV2PN")
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

# for a weight of 30 the decay over 10 secs is 0.0046369585134881175
# for a weight of 25 the decay over 10 secs is 0.003634116591918257
# for a weight of 20 the decay over 10 secs is 0.0027396942743642683
# for a weight of 15 the decay over 10 secs is 0.0019446108456619982
# for a weight of 10 the decay over 10 secs is 0.0012585058128120608
# for a weight of 5 the decay over 10 secs is 0.0003934396637488291
# good ff is 96
# ff of 75 = 98% 40=79% 80=99% 100=99.91
def compare_weight(path, start_time, end_time, decay_over_10sec = 0.0046369585134881175, decay_weight=30,fudge_factor = 80):
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
        and weight_at_start > weight_at_end):
            decay_weight = decay_weight + 1
        if ((weight_at_start[i] - weight_at_end[i]) * (decay_weight/weight_at_start[i]) > decay_over_10sec * fudge_factor
        and weight_at_start > weight_at_end):
            lower_than_start_weight = lower_than_start_weight + 1
        if ((weight_at_start[i] - weight_at_end[i]) * (decay_weight/weight_at_start[i]) > decay_over_10sec * fudge_factor
        and weight_at_start < weight_at_end):
            higher_than_start_weight = higher_than_start_weight + 1

    precent_higher = higher_than_start_weight/len(weight_at_start)*100
    precent_lower = lower_than_start_weight/len(weight_at_start)*100
    precent_decay = decay_weight/(len(weight_at_start))*100
    print("data for {}".format(path))
    print("Number of synapses that decayed {} {:.2f}%".format(decay_weight,precent_decay))
    print("Number of synpases that entered LTP {} {:.2f}%".format(higher_than_start_weight,precent_higher))
    print("Number of synpases that entered LTD {} {:.2f}%".format(lower_than_start_weight,precent_lower))
    print("\n")

print("Before tone trials")
compare_weight("outputECP/tone2PN_W.h5",start_time = 0,end_time=10000)
compare_weight("outputECP/bg_tone2PN_W.h5",start_time = 0, end_time=10000)

print("After tone trials")
compare_weight("outputECP/tone2PN_W.h5",start_time = 10000,end_time=20000)
compare_weight("outputECP/bg_tone2PN_W.h5",start_time = 10000, end_time=20000)

#compare_weight("outputECP_tone/tone2PV_W.h5",endtime=10000)
#compare_weight("outputECP_tone/bg_tone2PV_W.h5",endtime=10000)

#voltage = get_array('outputECP/v_report.h5')
#plt.plot(voltage)
#plt.show()


#plot_tone2pyr_noise()
#plot_tone2pyr()
#plotTone2PV()




def get_gids_and_data_arrays(path):
    file = h5py.File(path, 'r')
    cai_trace = file['report']['BLA']['data']

    time_ds = file['report/BLA/mapping/time']
    tstart = time_ds[0]
    tstop = time_ds[1]
    x_axis = np.linspace(tstart, tstop, len(cai_trace), endpoint=True)

    gids_ds = file['report/BLA/mapping/node_ids']
    index_ds = file['report/BLA/mapping/index_pointer']
    index_lookup = {gids_ds[i]: (index_ds[i], index_ds[i+1]) for i in range(len(gids_ds))}
    gid_list = []
    data_list = []
    for i in range(len(gids_ds)):
        var_indx = index_lookup[gids_ds[i]][0]
        data = cai_trace[:,var_indx]
        gid_list.append(gids_ds[i])
        data_list.append(data)
    return(gid_list,data_list)

    file = h5py.File('outputECP/tone2PN_W.h5')
    print(file['report/BLA/data'][:][0])

