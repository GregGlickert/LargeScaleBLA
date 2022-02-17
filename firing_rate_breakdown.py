import matplotlib.pyplot as plt
import h5py
import numpy as np
import pandas as pd

def spike_frequency_log_graph(spikes_df,node_set,ms,skip_ms=0,ax=None,n_bins=20, graph = None, y_max = None):
    print("Type : mean (std)")
    for node in node_set:
        if node['name'] != graph:
            pass
        else:
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
                ax.hist(spike_counts_per_second,n_bins,density=True,histtype='bar',label=label,color=c)
                ax.margins(0.5, 0.5)
        if ax:
            ax.set_xscale('log')
            ax.legend()

scale = 4
node_set_split = [
    {"name": "PN_A", "start": 0 * scale, "end": 568 * scale, "color": "blue"},
    {"name": "PN_C", "start": 569 * scale, "end": 799 * scale, "color": "olive"},
    {"name": "PV", "start": 800 * scale, "end": 892 * scale, "color": "purple"},
    {"name": "SOM", "start": 893 * scale, "end": 999 * scale, "color": "green"}
]

f = h5py.File('outputECP/spikes.h5')
spikes_df = pd.DataFrame(
    {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})

fig, axs = plt.subplots(4,1, figsize=(12, 6),tight_layout=True)
dt = 0.05
steps_per_ms = 1 / dt
skip_seconds = 5
skip_ms = skip_seconds * 1000
skip_n = int(skip_ms * steps_per_ms)
end_ms = 15000
spike_frequency_log_graph(spikes_df, node_set_split, end_ms, skip_ms=skip_ms, ax=axs[0], graph='PN_A')
spike_frequency_log_graph(spikes_df, node_set_split, end_ms, skip_ms=skip_ms, ax=axs[1], graph='PN_C')
spike_frequency_log_graph(spikes_df, node_set_split, end_ms, skip_ms=skip_ms, ax=axs[2], graph='SOM')
spike_frequency_log_graph(spikes_df, node_set_split, end_ms, skip_ms=skip_ms, ax=axs[3], graph='PV')
plt.show()