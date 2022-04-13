import matplotlib.pyplot as plt
import h5py
import numpy as np
import pandas as pd
import warnings



def spike_frequency_log_graph(spikes_df,node_set,ms,skip_ms=0,ax=None,n_bins=20, graph = None,most_exc=10 ):
    print("Type : mean (std)")
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

            label = "{} : {:.2f} ({:.2f})".format(node['name'],spikes_mean,spikes_std)
            print(label)
            c = "tab:" + node['color']
            if ax:
                #ax.hist(spike_counts_per_second,n_bins,density=True,histtype='bar',label=label,color=c)
                ax.hist(spike_counts_per_second, label=label, color=c)
                print('The cells with the most net exc fire like this with the left being the node id and the right being the '
                      'firing rate\n',most_exc_spike_counts_per_second)
                ax.margins(0.5, 0.5)
                ax.legend()
        if ax:
            ax.set_xscale('log')

def who_fired(spikes_df,node_set):
    for node in node_set:
        cells = range(node['start'], node['end'] + 1)  # +1 to be inclusive of last cell
        cell_spikes = spikes_df[spikes_df['node_ids'].isin(cells)]
        cell_spikes = cell_spikes.drop_duplicates(subset=['node_ids'])
        print(node['name'] + ' had this percent of cells fire')
        print(len(cell_spikes)/len(cells))


scale = 4
node_set_split = [
    {"name": "PN_A", "start": 0 * scale, "end": 568 * scale +3, "color": "blue"},
    {"name": "PN_C", "start": 569 * scale, "end": 799 * scale+3, "color": "olive"},
    {"name": "PV", "start": 800 * scale, "end": 892 * scale+3, "color": "purple"},
    {"name": "SOM", "start": 893 * scale, "end": 999 * scale + 4, "color": "green"}
]

f = h5py.File('outputECP/spikes.h5')
spikes_df = pd.DataFrame(
    {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})

fig, axs = plt.subplots(4,1, figsize=(12, 6),tight_layout=True)
dt = 0.1
steps_per_ms = 1 / dt
skip_seconds = 0
skip_ms = skip_seconds * 1000
skip_n = int(skip_ms * steps_per_ms)
end_ms = 15000

most_exc_PN_A = [257, 955, 367, 2005, 310]
most_exc_PN_C = [2467, 2747, 2559, 2407, 2559]
most_exc_PV = [3208, 3266, 3390, 3483, 3526]
most_exc_SOM = [3786, 3880, 3715, 3732, 3868]

spike_frequency_log_graph(spikes_df, node_set_split, end_ms, skip_ms=skip_ms, ax=axs[0], graph='PN_A', most_exc= most_exc_PN_A)
spike_frequency_log_graph(spikes_df, node_set_split, end_ms, skip_ms=skip_ms, ax=axs[1], graph='PN_C', most_exc= most_exc_PN_C)
spike_frequency_log_graph(spikes_df, node_set_split, end_ms, skip_ms=skip_ms, ax=axs[2], graph='SOM', most_exc= most_exc_SOM)
spike_frequency_log_graph(spikes_df, node_set_split, end_ms, skip_ms=skip_ms, ax=axs[3], graph='PV', most_exc= most_exc_PV)
plt.show()

#who_fired(spikes_df,node_set_split)