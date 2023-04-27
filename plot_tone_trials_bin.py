import h5py
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
plt.rcParams.update({'font.size': 16})

warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

scale = 5
node_set_split = [
    {"name": "PN_A", "start": 0 * scale, "end": 568 * scale , "color": "blue"},
    {"name": "PN_C", "start": 569 * scale, "end": 799 * scale, "color": "olive"},
    #{"name": "PN", "start": 0 * scale, "end": 799 * scale, "color": "olive"},
    {"name": "PV", "start": 800 * scale, "end": 899 * scale, "color": "purple"},
    {"name": "SOM", "start": 899 * scale, "end": 999 * scale, "color": "green"}
    #{"name": "VIP", "start": 1000 * scale, "end": 1106 * scale + 3, "color": "brown"}
]

def tone_firing_rate(cell_ids,spike_path,tone_start,tone_trials_count):
    fig, ax = plt.subplots(1,1, figsize=(12, 6),tight_layout=True)
    f = h5py.File(spike_path)
    spikes_df = pd.DataFrame(
        {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})
    start = tone_start
    end = tone_start + 500
    spikes = []
    for i in range(tone_trials_count):
        cell_spikes = spikes_df
        print(start,end)
        # skip the first few ms
        cell_spikes = cell_spikes[cell_spikes['timestamps'] > start]
        cell_spikes = cell_spikes[cell_spikes['timestamps'] < end]
        spike_counts = cell_spikes.node_ids.value_counts()
        spike_counts_per_second = spike_counts/0.5
        spikes.append(spike_counts_per_second)
        spikes_mean = spike_counts_per_second.mean()
        spikes_std = spike_counts_per_second.std()

        print("trial{} mean {:.2f} std {:.2f}".format(i,spikes_mean,spikes_std))

        start = start + 1500
        end = end + 1500

    return spikes

def plot(node_set=None, tone_start=None, spikes_df=None, ax=None,tone_trial_count = 8, title=0):
    for node in node_set:
        start = tone_start
        cells = range(node['start'], node['end'] + 1)  # +1 to be inclusive of last cell
        cell_spikes = spikes_df[spikes_df['node_ids'].isin(cells)]
        all_trials = pd.DataFrame(columns=['node_ids', 'timestamps'])
        end = start + 500
        for i in range(tone_trial_count):
            print(start, end)
            cell_spikes_temp = cell_spikes[cell_spikes['timestamps'] > start]
            cell_spikes_temp = cell_spikes_temp[cell_spikes['timestamps'] < end]
            all_trials = all_trials.append(cell_spikes_temp)
            start = start + 1500
            end = end + 1500

        spike_counts = all_trials.node_ids.value_counts()
        total_seconds = (tone_trial_count*500)/1000
        spike_counts = spike_counts / total_seconds

        spike_counts_mean = spike_counts.mean()
        spike_std = spike_counts.std()
        ax.bar(node['name'], spike_counts_mean, yerr=spike_std, align='center',color=node['color'],capsize=10,
               label='{} : {:.2f} ({:.2f})'.format(node['name'], spike_counts_mean, spike_std))
        #if ax == axs[0]:
        #    ax.set_ylabel("mean Hz during tone")
        ax.set_title(title)
        ax.set_ylim(0,60)
        ax.legend(loc=2, prop={'size': 8})


PN_array = range(800)
PV_array = range(800,900)
SOM_array = range(900,1000)
spike_path = 'new_runs/output_trials/spikes.h5'
f = h5py.File(spike_path)
spikes_df = pd.DataFrame(
    {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})

spike_path = 'new_runs/output_trials_0.5/spikes.h5'
f = h5py.File(spike_path)
spikes_df1 = pd.DataFrame(
    {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})

spike_path = 'new_runs/output_100_trials/spikes.h5'
f = h5py.File(spike_path)
spikes_df2 = pd.DataFrame(
    {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})




tone_start = 3000 # time the tones start
tone_trials_count = 3 # 15000 = 8 number of trials during the sim

fig, axs = plt.subplots(1,3, figsize=(21, 7),tight_layout=True,sharey=True)
#plot(node_set=node_set_split,tone_start=tone_start, spikes_df=spikes_df, ax=axs, tone_trial_count= tone_trials_count, title="baseline NMDA conductance")
#spikes = tone_firing_rate(PN_array,spike_path,tone_start,tone_trials_count)
#plt.hist(spikes)
#plt.show()
plot(node_set=node_set_split,tone_start=3000, spikes_df=spikes_df, ax=axs[0], tone_trial_count= 5, title="baseline NMDA conductance")
plot(node_set=node_set_split,tone_start=3000, spikes_df=spikes_df1, ax=axs[1], tone_trial_count= 5, title="50% block")
plot(node_set=node_set_split,tone_start=3000, spikes_df=spikes_df2, ax=axs[2], tone_trial_count= 5, title="100% block")
plt.show()
#plot(node_set=node_set_split,tone_start=30000, spikes_df=spikes_df, ax=axs, tone_trial_count= 5, title="baseline NMDA conductance")
#plt.show()