import matplotlib.pyplot as plt
import h5py
import numpy as np
import pandas as pd

f = h5py.File('outputECP1/spikes.h5')
spikes_df1 = pd.DataFrame(
    {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})
f = h5py.File('outputECP2/spikes.h5')
spikes_df2 = pd.DataFrame(
    {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})
f = h5py.File('outputECP3/spikes.h5')
spikes_df3 = pd.DataFrame(
    {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})

scale = 4
node_set_split = [
    {"name": "PN_A", "start": 0 * scale, "end": 568 * scale + 3, "color": "blue"},
    {"name": "PN_C", "start": 569 * scale, "end": 799 * scale+ 3, "color": "olive"},
    {"name": "PV", "start": 800 * scale, "end": 892 * scale+ 3, "color": "purple"},
    {"name": "SOM", "start": 893 * scale, "end": 999 * scale + 4, "color": "green"},
    {"name": "VIP", "start": 1000 * scale, "end": 1106 * scale + 3, "color": "brown"}
]

fig, axs = plt.subplots(1,3, figsize=(12, 6),tight_layout=True,sharey=True)

def plot(node_set,skip_ms,spikes_df,ax,title=0 ):
    for node in node_set:
        cells = range(node['start'], node['end'] + 1)  # +1 to be inclusive of last cell
        cell_spikes = spikes_df[spikes_df['node_ids'].isin(cells)]
        cell_spikes = cell_spikes[cell_spikes['timestamps'] > skip_ms]
        spike_counts = cell_spikes.node_ids.value_counts()
        spike_counts_mean = spike_counts.mean()
        spike_std = spike_counts.std()
        ax.bar(node['name'], spike_counts_mean, yerr=spike_std, align='center',ecolor='black',capsize=10,
               label='{} : {:.2f} ({:.2f})'.format(node['name'], spike_counts_mean, spike_std))
        label = "{} : {:.2f} ({:.2f})".format(node['name'], spike_counts_mean, spike_std)
        if ax == axs[0]:
            ax.set_ylabel("mean number of spikes in 5 seconds")
        ax.set_title(title)
        ax.legend(loc=2, prop={'size': 8})

plot(node_set=node_set_split,skip_ms=10000,spikes_df=spikes_df1,ax=axs[0],title="baseline NMDA conductance")
plot(node_set=node_set_split,skip_ms=10000,spikes_df=spikes_df2,ax=axs[1],title='half NMDA conductance')
plot(node_set=node_set_split,skip_ms=10000,spikes_df=spikes_df3,ax=axs[2],title='zero NMDA conductance')
plt.ylim(0,70)
plt.show()