import matplotlib.pyplot as plt
import h5py
import numpy as np
import pandas as pd
import statistics
import warnings



def spike_frequency_log_graph(spikes_df,node_set,ms,skip_ms=0,ax=None,n_bins=20, graph = None,most_exc=10 ):
    for node in node_set:
        if node['name'] != graph:
            pass
        else:
            most_exc_cells = spikes_df[spikes_df['node_ids'].isin(most_exc)]
            most_exc_cell_spikes = most_exc_cells[most_exc_cells['timestamps']>skip_ms]
            most_exc_spike_counts = most_exc_cell_spikes.node_ids.value_counts()
            total_seconds = (ms-skip_ms)/1000
            most_exc_spike_counts_per_second = most_exc_spike_counts / total_seconds

            cells = range(node['start'],node['end']+1) #+1 to be inclusive of last cell
            cell_spikes = spikes_df[spikes_df['node_ids'].isin(cells)]

            #skip the first few ms
            cell_spikes = cell_spikes[cell_spikes['timestamps']>skip_ms]
            spike_counts = cell_spikes.node_ids.value_counts()
            total_seconds = (ms-skip_ms)/1000
            spike_counts_per_second = spike_counts / total_seconds

            spikes_mean = spike_counts_per_second.mean()
            spikes_std = spike_counts_per_second.std()
            spike_median = statistics.median(spike_counts_per_second)

            label = "{} : mean {:.2f} std ({:.2f}) median {:.2f}".format(node['name'],spikes_mean,spikes_std,spike_median)
            print(label)
            c = node['color']
            if ax:
                #ax.hist(spike_counts_per_second,n_bins,density=True,histtype='bar',label=label,color=c)
                ax.hist(spike_counts_per_second, label=label, color=c)
                locs = ax.get_yticks()
                #print(locs)
                ax.set_yticks(locs, np.round(locs / len(spike_counts_per_second), 3))

                #print('The cells with the most net exc fire like this with the left being the node id and the right being the '
                #      'firing rate\n',most_exc_spike_counts_per_second)
                ax.margins(0.5, 0.5)
                ax.legend()
        #if ax:
            #ax.set_xscale('log')

def who_fired(spikes_df,node_set):
    for node in node_set:
        cells = range(node['start'], node['end'] + 1)  # +1 to be inclusive of last cell
        cell_spikes = spikes_df[spikes_df['node_ids'].isin(cells)]
        cell_spikes = cell_spikes.drop_duplicates(subset=['node_ids'])
        print(node['name'] + ' had this percent of cells fire')
        print(len(cell_spikes)/len(cells))

def check_PN_rate(spike_df, skip_ms=0, ms = 0):
    type_A = range(0, 2275)
    type_C = range(2276, 3199)
    both = range(0, 3199)

    type_A_spikes = spike_df[spike_df['node_ids'].isin(type_A)]
    type_C_spikes = spike_df[spike_df['node_ids'].isin(type_C)]
    PN_spikes = spike_df[spike_df['node_ids'].isin(both)]

    type_A_spikes = type_A_spikes[type_A_spikes['timestamps'] > skip_ms]
    type_A_spike_counts = type_A_spikes.node_ids.value_counts()
    total_seconds = (ms - skip_ms) / 1000
    type_A_spike_counts_per_second = type_A_spike_counts / total_seconds

    type_A_spikes_mean = type_A_spike_counts_per_second.mean()
    type_A_spikes_std = type_A_spike_counts_per_second.std()

    type_C_spikes = type_C_spikes[type_C_spikes['timestamps'] > skip_ms]
    type_C_spike_counts = type_C_spikes.node_ids.value_counts()
    type_C_spike_counts_per_second = type_C_spike_counts / total_seconds

    type_C_spikes_mean = type_C_spike_counts_per_second.mean()
    type_C_spikes_std = type_C_spike_counts_per_second.std()

    PN_spikes = PN_spikes[PN_spikes['timestamps'] > skip_ms]
    PN_spike_counts = PN_spikes.node_ids.value_counts()
    PN_spike_counts_per_second = PN_spike_counts / total_seconds

    PN_spikes_mean = PN_spike_counts_per_second.mean()
    PN_spikes_std = PN_spike_counts_per_second.std()

    #print("Type A mean", round(type_A_spikes_mean,2))
    #print("Type A std", round(type_A_spikes_std,2))
    #print("Type C mean", round(type_C_spikes_mean,2))
    #print("Type C std", round(type_C_spikes_std,2))
    print("Total PN mean", round(PN_spikes_mean,2))
    print("total PN std", round(PN_spikes_std,2))

    type_A_over_1hz = 0
    type_C_over_1hz = 0
    PN_over_1hz = 0
    temp = type_A_spike_counts_per_second.to_numpy()
    for i in range(temp.shape[0]):
        if temp[i] > 1:
            type_A_over_1hz = type_A_over_1hz + 1
    over1 = round(type_A_over_1hz / temp.shape[0], 2)
    print("Of the PN type A cells that fired {}% cells fired above 1 Hz".format(over1))

    temp = type_C_spike_counts_per_second.to_numpy()
    for i in range(temp.shape[0]):
        if temp[i] > 1:
            type_C_over_1hz = type_C_over_1hz + 1
    over1 = round(type_C_over_1hz / temp.shape[0], 2)
    print("Of the PN type C cells that fired {}% cells fired above 1 Hz".format(over1))

    temp = PN_spike_counts_per_second.to_numpy()
    for i in range(temp.shape[0]):
        if temp[i] > 1:
            PN_over_1hz = PN_over_1hz + 1
    over1 = round(PN_over_1hz / temp.shape[0], 2)
    print("Of the PN cells that fired {}% cells fired above 1 Hz".format(over1))

scale = 4
node_set_split = [
    {"name": "Pyr_A", "start": 0 * scale, "end": 568 * scale + 3, "color": "#ff1100"},
    {"name": "Pyr_C", "start": 569 * scale, "end": 799 * scale+ 3, "color": "#d63904"},
    {"name": "Pyr", "start": 0 * scale, "end": 799 * scale + 3, "color": "#bf1408"},
    {"name": "FSI", "start": 800 * scale, "end": 892 * scale+ 3, "color": "#05acfa"},
    {"name": "LTS", "start": 893 * scale, "end": 999 * scale + 4, "color": "#138bc2"},
    #{"name": "VIP", "start": 1000 * scale, "end": 1106 * scale + 3, "color": "brown"}
    {"name": "IN", "start": 800 * scale, "end": 999 * scale + 4, "color": "#057ffa"}
]

f = h5py.File('baseline/spikes.h5')
spikes_df = pd.DataFrame(
    {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})

fig, axs = plt.subplots(6,1, figsize=(12, 6),tight_layout=True)
dt = 0.1
steps_per_ms = 1 / dt
skip_seconds = 0
skip_ms = skip_seconds * 1000
skip_n = int(skip_ms * steps_per_ms)
end_ms = 10000

most_exc_PN_A = [257, 955, 367, 2005, 310]
most_exc_PN_C = [2467, 2747, 2559, 2407, 2559]
most_exc_PV = [3208, 3266, 3390, 3483, 3526]
most_exc_SOM = [3786, 3880, 3715, 3732, 3868]
most_exc_VIP = [0, 0, 0, 0, 0]

spike_frequency_log_graph(spikes_df, node_set_split, end_ms, skip_ms=skip_ms, ax=axs[0], graph='Pyr_A', most_exc= most_exc_PN_A)
spike_frequency_log_graph(spikes_df, node_set_split, end_ms, skip_ms=skip_ms, ax=axs[1], graph='Pyr_C', most_exc= most_exc_PN_C)
spike_frequency_log_graph(spikes_df, node_set_split, end_ms, skip_ms=skip_ms, ax=axs[2], graph='Pyr', most_exc= most_exc_PN_C)
spike_frequency_log_graph(spikes_df, node_set_split, end_ms, skip_ms=skip_ms, ax=axs[3], graph='FSI', most_exc= most_exc_SOM)
spike_frequency_log_graph(spikes_df, node_set_split, end_ms, skip_ms=skip_ms, ax=axs[4], graph='LTS', most_exc= most_exc_PV)
spike_frequency_log_graph(spikes_df, node_set_split, end_ms, skip_ms=skip_ms, ax=axs[5], graph='IN',most_exc=most_exc_VIP)

plt.show()