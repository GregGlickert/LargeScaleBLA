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

def compare_weight(path,endtime, decay_over_10sec = 0.0046369585134881175, decay_weight=30,fudge_factor = 80):
    W = get_array(path=path)
    weight_at_start = []
    weight_at_end = []
    for i in range(len(W[0])):
        weight_at_start.append(W[0][i])
    for i in range(len(W[0])):
        weight_at_end.append(W[(endtime*10)-1][i])
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
    return(decay_weight,higher_than_start_weight,lower_than_start_weight)

fig, ax = plt.subplots(2,2, figsize=(12, 6),tight_layout=True,sharey=True)

decay,LTP,LTD = compare_weight("outputECP_tone/tone2PN_W.h5",endtime=10000)
ax[0][0].bar("decay",decay)
ax[0][0].bar("LTP",LTP)
ax[0][0].bar("LTD",LTD)
ax[0][0].set_title("PN tone trials")
decay,LTP,LTD = compare_weight("outputECP_tone/bg_tone2PN_W.h5",endtime=10000)
ax[1][0].bar("decay",decay)
ax[1][0].bar("LTP",LTP)
ax[1][0].bar("LTD",LTD)
ax[1][0].set_title("PN tone noise")
decay,LTP,LTD = compare_weight("outputECP_tone/tone2PV_W.h5",endtime=10000)
ax[0][1].bar("decay",decay)
ax[0][1].bar("LTP",LTP)
ax[0][1].bar("LTD",LTD)
ax[0][1].set_title("PV tone trials")
decay,LTP,LTD = compare_weight("outputECP_tone/bg_tone2PV_W.h5",endtime=10000)
ax[1][1].bar("decay",decay)
ax[1][1].bar("LTP",LTP)
ax[1][1].bar("LTD",LTD)
ax[1][1].set_title("PV tone noise")
plt.show()


