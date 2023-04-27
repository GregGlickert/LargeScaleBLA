import matplotlib.pyplot as plt
import h5py
import numpy as np
import pandas as pd
import statistics
import warnings

warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

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
                #ax.set_yticks(locs, np.round(locs / len(spike_counts_per_second), 3))

                #print('The cells with the most net exc fire like this with the left being the node id and the right being the '
                #      'firing rate\n',most_exc_spike_counts_per_second)
                ax.margins(0.5, 0.5)
                ax.legend()
        #if ax:
            #ax.set_xscale('log')

def spike_frequency_histogram(spikes_df,node_set,ms,skip_ms=0,ax=None,n_bins=10):
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
        c = node['color']
        if ax:
            ax.hist(spike_counts_per_second,n_bins,density=True,histtype='bar',label=label,color=c)
    if ax:
        #ax.set_xscale('log')
        ax.set_xlabel('Hz')
        ax.set_ylabel('Percentage(#)')
        ax.legend() 

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

def tone_trial_plot(node_set=None, tone_start=None, spikes_df=None, ax=None,tone_trial_count = 8, title=0,graph = None):
    for node in node_set:
        if node['name'] != graph:
            pass
        else:
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
            spikes_mean = spike_counts.mean()
            spikes_std = spike_counts.std()
            spike_median = statistics.median(spike_counts)

            c = node['color']
            label = "{} : mean {:.2f} std ({:.2f}) median {:.2f}".format(node['name'],spikes_mean,spikes_std,spike_median)
            ax.hist(spike_counts, label=label, color=c, bins=10)
            ax.margins(0.5, 0.5)
            ax.legend()

scale = 5
node_set_split = [
    {"name": "PN_A", "start": 0 * scale, "end": 568 * scale , "color": "blue"},
    {"name": "PN_C", "start": 569 * scale, "end": 799 * scale, "color": "olive"},
    #{"name": "PN", "start": 0 * scale, "end": 799 * scale, "color": "olive"},
    {"name": "PV", "start": 800 * scale, "end": 899 * scale, "color": "purple"},
    {"name": "SOM", "start": 899 * scale, "end": 999 * scale, "color": "green"}
    #{"name": "VIP", "start": 1000 * scale, "end": 1106 * scale + 3, "color": "brown"}
]

f = h5py.File('outputECP_trials_e/spikes.h5')
spikes_df = pd.DataFrame(
    {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})

fig, axs = plt.subplots(2,2, figsize=(12, 6),tight_layout=True)
dt = 0.1
steps_per_ms = 1 / dt
skip_seconds = 0
skip_ms = skip_seconds * 1000
skip_n = int(skip_ms * steps_per_ms)
end_ms = 47000

most_exc_PN_A = [257, 955, 367, 2005, 310]
most_exc_PN_C = [2467, 2747, 2559, 2407, 2559]
most_exc_PV = [3208, 3266, 3390, 3483, 3526]
most_exc_SOM = [3786, 3880, 3715, 3732, 3868]
most_exc_VIP = [0, 0, 0, 0, 0]

def each_cell_firing_rate():
    spike_frequency_log_graph(spikes_df, node_set_split, end_ms, skip_ms=skip_ms, ax=axs[0,0], graph='PN_A', most_exc= most_exc_PN_A)
    spike_frequency_log_graph(spikes_df, node_set_split, end_ms, skip_ms=skip_ms, ax=axs[0,1], graph='PN_C', most_exc= most_exc_PN_C)   
    spike_frequency_log_graph(spikes_df, node_set_split, end_ms, skip_ms=skip_ms, ax=axs[1,0], graph='PV', most_exc= most_exc_SOM)
    spike_frequency_log_graph(spikes_df, node_set_split, end_ms, skip_ms=skip_ms, ax=axs[1,1], graph='SOM', most_exc= most_exc_PV)
    plt.suptitle("Firing rates during baseline")
    plt.show()

def each_cell_firing_tone(tone_start = 3000):
    tone_trial_plot(node_set=node_set_split,tone_start=tone_start, spikes_df=spikes_df, ax=axs[0,0], tone_trial_count= 10, title="baseline NMDA conductance",graph='PN_A')
    tone_trial_plot(node_set=node_set_split,tone_start=tone_start, spikes_df=spikes_df, ax=axs[0,1], tone_trial_count= 10, title="baseline NMDA conductance",graph='PN_C')
    tone_trial_plot(node_set=node_set_split,tone_start=tone_start, spikes_df=spikes_df, ax=axs[1,0], tone_trial_count= 10, title="baseline NMDA conductance",graph='PV')
    tone_trial_plot(node_set=node_set_split,tone_start=tone_start, spikes_df=spikes_df, ax=axs[1,1], tone_trial_count= 10, title="baseline NMDA conductance",graph='SOM')
    plt.suptitle("Firing rates during tone trials at time " + str(tone_start))
    plt.show()

# uncomment to plot all of them in one graph
#fig, axs = plt.subplots(1,1, figsize=(12, 6),tight_layout=True)
#spike_frequency_histogram(spikes_df,node_set_split,end_ms,skip_ms,axs,n_bins=10)

# to plot each cell type in a different graph
#each_cell_firing_rate()

each_cell_firing_tone(tone_start=33000)
