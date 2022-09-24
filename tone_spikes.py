import matplotlib.pyplot as plt
import h5py
import numpy as np
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=UserWarning)

f = h5py.File('0%tone/spikes.h5')
spikes_df1 = pd.DataFrame(
    {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})
f = h5py.File('50%tone/spikes.h5')
spikes_df2 = pd.DataFrame(
    {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})
f = h5py.File('75%tone/spikes.h5')
spikes_df3 = pd.DataFrame(
    {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})



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


fig, axs = plt.subplots(1,3, figsize=(12, 6),tight_layout=True,sharey=True)
fig.suptitle("7 500ms Tone pips", fontsize=15)
def plot(node_set=None, start=None, end=None, spikes_df=None, ax=None, title=0):
    for node in node_set:
        cells = range(node['start'], node['end'] + 1)  # +1 to be inclusive of last cell
        cell_spikes = spikes_df[spikes_df['node_ids'].isin(cells)]
        if start==None:
            all_trials = pd.DataFrame(columns=['node_ids', 'timestamps'])
            start = 500
            end = 1000
            time = 0
            for i in range(7):
                time = time + 500
                print(start, end)
                cell_spikes_temp = cell_spikes[cell_spikes['timestamps'] > start]
                cell_spikes_temp = cell_spikes_temp[cell_spikes['timestamps'] < end]
                all_trials = all_trials.append(cell_spikes_temp)
                start = start + 1500
                end = end + 1500

            spike_counts = all_trials.node_ids.value_counts()
            total_seconds = (3500)/1000
            spike_counts = spike_counts / total_seconds

            spike_counts_mean = spike_counts.mean()
            spike_std = spike_counts.std()
            start = None # to get if statement again kinda a lazy way
        else:
            cell_spikes = cell_spikes[cell_spikes['timestamps'] > start]
            cell_spikes = cell_spikes[cell_spikes['timestamps'] < end]
            spike_counts = cell_spikes.node_ids.value_counts()
            total_seconds = (end-start)/1000
            spike_counts = spike_counts / total_seconds
            spike_counts_mean = spike_counts.mean()
            spike_std = spike_counts.std()
        ax.bar(node['name'], spike_counts_mean, yerr=spike_std, align='center',color=node['color'],capsize=10,
               label='{} : {:.2f} ({:.2f})'.format(node['name'], spike_counts_mean, spike_std))
        if ax == axs[0]:
            ax.set_ylabel("mean Hz during tone")
        ax.set_title(title)
        ax.set_ylim(0,30)
        ax.legend(loc=2, prop={'size': 8})

#plot(node_set=node_set_split,start=500, end=1000, spikes_df=spikes_df, ax=axs[0], title="first tone")
#plot(node_set=node_set_split,start=9500, end=10000, spikes_df=spikes_df, ax=axs[1], title="last tone")
plot(node_set=node_set_split,start=None, end=None, spikes_df=spikes_df1, ax=axs[0], title="baseline NMDA conductance")
plot(node_set=node_set_split,start=None, end=None, spikes_df=spikes_df2, ax=axs[1], title="50% NMDA blocked")
plot(node_set=node_set_split,start=None, end=None, spikes_df=spikes_df3, ax=axs[2], title="75% NMDA blocked")
#plot(node_set=node_set_split,start=None, end=None, spikes_df=spikes_df5, ax=axs[1], title="50% blocked")

plt.show()