from bmtk.utils.reports.compartment import CompartmentReport
import numpy as np
from tqdm import tqdm
import h5py
import pandas as pd
import matplotlib.pyplot as plt

def get_data():
    report = CompartmentReport("outputECP_trials/tone2PN_dep_flag.h5")
    cells = report.node_ids()
    nodes = []
    zero_count = []
    for i in tqdm(range(len(report.node_ids()))):
        data = report.data(node_id=i)
        zero_count.append(np.count_nonzero(data)) 
        nodes.append(i)

    def get_firing_rate(spike_path,node_id,total_seconds):
        f = h5py.File(spike_path)
        spikes_df = pd.DataFrame({'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})
        cell_spikes = spikes_df[spikes_df['node_ids'].isin(node_id)]
        spike_counts = cell_spikes.node_ids.value_counts()
        spike_counts_per_second = spike_counts / total_seconds
        return spike_counts_per_second


    spikes = get_firing_rate('outputECP_trials/spikes.h5',node_id=nodes,total_seconds=47)
    all_data = list(zip(nodes,zero_count,spikes))
    df = pd.DataFrame(all_data,columns=['node_id','zero_count', 'spikes'])
    df.to_csv("LTD_vs_HZ.csv")


def plot():
    df = pd.read_csv("LTD_vs_HZ.csv")
    hz = df['spikes']
    LTD = df['zero_count'].to_numpy()
    LTD = 470000 - LTD

    plt.bar(hz,LTD)
    plt.xlabel("Firing Rate")
    plt.ylabel("LTD rate")
    plt.title("LTD rate vs HZ (lower on LTD scale means more LTD data is messed up right now)")
    plt.show()

#get_data()

plot()