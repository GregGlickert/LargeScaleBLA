from bmtk.analyzer.spike_trains import plot_raster, plot_rates_boxplot, plot_rates
from bmtk.analyzer.compartment import plot_traces
from bmtk.analyzer.spike_trains import to_dataframe
import matplotlib.pyplot as plt
import h5py
import numpy as np
import pandas as pd

def raster(spikes_df, node_set, start=0,end=80000, ax=None):
    spikes_df = spikes_df[spikes_df['timestamps'] > start]
    spikes_df = spikes_df[spikes_df['timestamps'] < end]
    for node in node_set:
        cells = range(node['start'], node['end'] + 1)  # +1 to be inclusive of last cell
        cell_spikes = spikes_df[spikes_df['node_ids'].isin(cells)]

        ax.scatter(cell_spikes['timestamps'], cell_spikes['node_ids'],
                   c='tab:' + node['color'], s=2, label=node['name'])

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(reversed(handles), reversed(labels),loc='lower right')
    ax.grid(False)

def spike_frequency_bar_graph(spikes_df, node_set, ms, start=0, end=80000, ax=None):
    mean = []
    name = []
    labels = []
    for node in node_set:
        cells = range(node['start'], node['end'] + 1)  # +1 to be inclusive of last cell
        cell_spikes = spikes_df[spikes_df['node_ids'].isin(cells)]

        # skip the first few ms
        cell_spikes = cell_spikes[cell_spikes['timestamps'] > start]
        cell_spikes = cell_spikes[cell_spikes['timestamps'] < end]
        spike_counts = cell_spikes.node_ids.value_counts()
        total_seconds = (ms) / 1000
        spike_counts_per_second = spike_counts / total_seconds

        spikes_mean = spike_counts_per_second.mean()
        spikes_std = spike_counts_per_second.std()

        label = "{} : {:.2f} ({:.2f})".format(node['name'], spikes_mean, spikes_std)
        #print(label)
        c = "tab:" + node['color']
        if ax:
            mean.append(spikes_mean)
            name.append(node['name'])
            labels.append(label)
            ax.bar(node['name'], spikes_mean,label=label,color=c)


    if ax:
        ax.legend()

def spike_frequency_log_graph(spikes_df,node_set,ms,skip_ms=0,ax=None,n_bins=10):
    print("Type : mean (std)")
    for node in node_set:
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
    if ax:
        ax.set_xscale('log')
        ax.legend()

scale = 4
node_set = [
    {"name": "PN", "start": 0*scale, "end": 799*scale, "color": "blue"},
    {"name": "PV", "start": 800*scale, "end": 892*scale, "color": "gray"},
    {"name": "SOM", "start": 893*scale, "end": 999*scale, "color": "green"}
]

node_set_split = [
    {"name": "PN_A", "start": 0 * scale, "end": 568 * scale + 3, "color": "blue"},
    {"name": "PN_C", "start": 569 * scale, "end": 799 * scale+ 3, "color": "olive"},
    {"name": "PV", "start": 800 * scale, "end": 892 * scale+ 3, "color": "purple"},
    {"name": "SOM", "start": 893 * scale, "end": 999 * scale + 4, "color": "green"},
    {"name": "VIP", "start": 1000 * scale, "end": 1106 * scale + 3, "color": "brown"}
]

f = h5py.File('outputECP/spikes.h5')
spikes_df = pd.DataFrame({'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})

fig, axs = plt.subplots(1, 2, figsize=(15, 6))
start1 = 0
end1 = 15000
dt = 0.1
steps_per_ms = 1 / dt
skip_seconds = 5
skip_ms = skip_seconds * 1000
skip_n = int(skip_ms * steps_per_ms)
end_ms = 10000
raster(spikes_df, node_set_split, start=start1, end=end1, ax=axs[0])
spike_frequency_bar_graph(spikes_df,node_set_split,start=start1, end=end1, ax=axs[1], ms=(end1-start1))
#spike_frequency_log_graph(spikes_df,node_set,end_ms,skip_ms=skip_ms,ax=axs[1])
plt.show()
#trace = plot_traces(report_path='outputECP/v_report.h5',node_ids=[3999])

#rates = plot_rates_boxplot(config_file='simulation_config.json', group_by='pop_name',times=(600,900))

#file = "network/shock_BLA_edges.h5"
#file = h5py.File(file,'r')
#print((file['edges']['shock_to_BLA']['target_node_id'][:]))
