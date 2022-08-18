import matplotlib.pyplot as plt
import h5py
import numpy as np
import pandas as pd

f = h5py.File('baseline/spikes.h5')
spikes_df1 = pd.DataFrame(
    {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})
f = h5py.File('50%baseline/spikes.h5')
spikes_df2 = pd.DataFrame(
    {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})
f = h5py.File('75%baseline/spikes.h5')
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
fig.suptitle("Spontaneous case", fontsize=15)
def plot(node_set,skip_ms,spikes_df,ax,title=0):
    spikes = []
    for node in node_set:
        cells = range(node['start'], node['end'] + 1)  # +1 to be inclusive of last cell
        cell_spikes = spikes_df[spikes_df['node_ids'].isin(cells)]
        cell_spikes = cell_spikes[cell_spikes['timestamps'] > skip_ms]
        spike_counts = cell_spikes.node_ids.value_counts()
        total_seconds = (10000) / 1000
        spike_counts = spike_counts / total_seconds
        spikes.append(spike_counts)
        spike_counts_mean = spike_counts.mean()
        spike_std = spike_counts.std()
        ax.bar(node['name'], spike_counts_mean, yerr=spike_std, align='center',color=node['color'],capsize=10,
               label='{} : {:.2f} ({:.2f})'.format(node['name'], spike_counts_mean, spike_std))
        label = "{} : {:.2f} ({:.2f})".format(node['name'], spike_counts_mean, spike_std)
        if ax == axs[0]:
            ax.set_ylabel("mean firing rate(Hz) in 5 seconds")
        ax.set_title(title)
        ax.legend(loc=2, prop={'size': 8})
    return spikes


spike_w_NMDA=plot(node_set=node_set_split,skip_ms=0,spikes_df=spikes_df1,ax=axs[0],title="baseline NMDA conductance")
spike_wo_NMDA=plot(node_set=node_set_split,skip_ms=0,spikes_df=spikes_df2,ax=axs[1],title=' 50% NMDA block')
spike_wo_NMDA=plot(node_set=node_set_split,skip_ms=0,spikes_df=spikes_df3,ax=axs[2],title=' 75% NMDA block')

plt.ylim(0,6)

#PN_spikes = (spike_w_NMDA[0].mean()+spike_w_NMDA[1].mean()) - (spike_wo_NMDA[0].mean()+spike_wo_NMDA[1].mean())
#PV_spikes = (spike_w_NMDA[2].mean() - spike_wo_NMDA[2].mean())
#SOM_spikes = (spike_w_NMDA[3].mean() - spike_wo_NMDA[3].mean())

#print("The PN mean spikes changed by {:1f} when comparing baseline and CPP".format(PN_spikes))
#print("The FSI mean spikes changed by {:1f} when comparing baseline and CPP".format(PV_spikes))
#print("The LTS mean spikes changed by {:1f} when comparing baseline and CPP".format(SOM_spikes))

plt.show()