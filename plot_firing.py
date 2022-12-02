from scipy.signal import hanning,welch,decimate
import h5py
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
plt.rcParams.update({'font.size': 20})

def spike_frequency_histogram(spikes_df, node_set, ms, skip_ms=0, ax=None, n_bins=10):
    print("Type : mean (std)")
    for node in node_set:
        cells = range(node['start'], node['end'] + 1)  # +1 to be inclusive of last cell
        cell_spikes = spikes_df[spikes_df['node_ids'].isin(cells)]

        # skip the first few ms
        cell_spikes = cell_spikes[cell_spikes['timestamps'] > skip_ms]
        spike_counts = cell_spikes.node_ids.value_counts()
        total_seconds = (ms - skip_ms) / 1000
        spike_counts_per_second = spike_counts / total_seconds

        spikes_mean = spike_counts_per_second.mean()
        spikes_std = spike_counts_per_second.std()

        label = "{} : {:.2f} ({:.2f})".format(node['name'], spikes_mean, spikes_std)
        print(label)
        c = node['color']
        if ax:
            ax.hist(spike_counts_per_second, n_bins, histtype='bar', label=label, color=c)
    if ax:
        #ax.set_xscale('log')
        ax.legend()
        ax.set_xlabel('Hz')
        ax.set_ylabel('amount of cells')

scale = 4
node_set_split = [
    {"name": "Pyr_A", "start": 0 * scale, "end": 568 * scale + 3, "color": "#ff1100"},
    {"name": "Pyr_C", "start": 569 * scale, "end": 799 * scale+ 3, "color": "#d63904"},
    #{"name": "Pyr", "start": 0 * scale, "end": 799 * scale + 3, "color": "#bf1408"},
    {"name": "FSI", "start": 800 * scale, "end": 892 * scale+ 3, "color": "#05acfa"},
    {"name": "LTS", "start": 893 * scale, "end": 999 * scale + 4, "color": "#138bc2"},
    #{"name": "VIP", "start": 1000 * scale, "end": 1106 * scale + 3, "color": "brown"}
    #{"name": "IN", "start": 800 * scale, "end": 999 * scale + 4, "color": "#057ffa"}
]

f = h5py.File('outputECP_NMDA_BASELINE/spikes.h5')
#f = h5py.File('outputECP_NMDA_baseline/spikes.h5')
spikes_df = pd.DataFrame(
    {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})

fig, axs = plt.subplots(1,1, figsize=(12, 6),tight_layout=True)
dt = 0.1
steps_per_ms = 1 / dt
skip_seconds = 0
skip_ms = skip_seconds * 1000
skip_n = int(skip_ms * steps_per_ms)
end_ms = 12500

spike_frequency_histogram(spikes_df, node_set_split, end_ms, skip_ms=skip_ms, ax=axs)
plt.show()