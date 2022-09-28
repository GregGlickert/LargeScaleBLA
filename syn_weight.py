from re import L
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

def plot_PN2PN():
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

def plot_PN2SOM():
    fig, ax = plt.subplots(2,1, figsize=(12, 6),tight_layout=True)
    weight_path = "outputECP/PN2SOM_W.h5"
    cai_path = "outputECP/PN2SOM_cai.h5"
    weight_array = get_array(weight_path)
    cai_array = get_array(cai_path)
    cai_array[:] = [x * 1000 for x in cai_array] #to fix units
    ax[0].plot(weight_array)
    ax[1].plot(cai_array)
    plt.suptitle("PN2SOM")
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

plot_PN2PN()

plot_PN2PV()
 
plot_PN2SOM()

#check_distro('outputECP/PN2SOM.h5',10000)


