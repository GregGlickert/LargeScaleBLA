import random
import h5py
import numpy as np
import pandas as pd
import warnings
import matplotlib.pyplot as plt
from sympy import re
from tqdm import tqdm
from bmtk.analyzer.spike_trains import plot_rates
from bmtk.analyzer.compartment import plot_traces


random.seed(123412)
np.random.seed(123412)
warnings.simplefilter(action='ignore', category=UserWarning)
tone_synapses = random.sample(range(4000), 2800)

random_PN_A_array = random.sample(range(2276), 30)
random_PN_C_array = random.sample(range(2277,3199),30)
print(random_PN_C_array)

random_PV_array = random.sample(range(3200,3568),30)
random_SOM_array = random.sample(range(3569,4000),30)


def spontaneous_firing_rate(cell_ids,spike_path,skip_ms):
    f = h5py.File(spike_path)
    spikes_df = pd.DataFrame(
        {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})
    cell_spikes = spikes_df[spikes_df['node_ids'].isin(cell_ids)]
    cell_spikes = cell_spikes[cell_spikes['timestamps'] > skip_ms]
    spike_counts = cell_spikes.node_ids.value_counts()
    total_seconds = (10000-skip_ms) / 1000
    spike_counts = spike_counts / total_seconds
    spike_counts_mean = spike_counts.mean()
    spike_std = spike_counts.std()
    print("spike mean during spontaneous is {:.2f} with std of {:.2f}".format(spike_counts_mean,spike_std))

def tone_trials_firing_rate_look_at(cell_ids,spike_path):
    """
    f = h5py.File(spike_path)
    spikes_df = pd.DataFrame(
        {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})
    cell_spikes = spikes_df[spikes_df['node_ids'].isin(cell_ids)]
    start = 500
    end = 1000
    start_of_tone_trials = pd.DataFrame(columns=['node_ids', 'timestamps'])
    for i in range(2): # first two tone trials
        #print(start, end)
        cell_spikes_temp = cell_spikes[cell_spikes['timestamps'] > start]
        cell_spikes_temp = cell_spikes_temp[cell_spikes['timestamps'] < end]
        start_of_tone_trials = start_of_tone_trials.append(cell_spikes_temp)
        start = start + 1500
        end = end + 1500
    end_of_tone_trials = pd.DataFrame(columns=['node_ids', 'timestamps'])
    start = 12500
    end = 13000
    for i in range(2): # for last two tone trials
        #print(start, end)
        cell_spikes_temp = cell_spikes[cell_spikes['timestamps'] > start]
        cell_spikes_temp = cell_spikes_temp[cell_spikes['timestamps'] < end]
        end_of_tone_trials = end_of_tone_trials.append(cell_spikes_temp)
        start = start + 1500
        end = end + 1500

    spike_count_at_start = start_of_tone_trials.node_ids.value_counts()
    total_seconds = (1000)/1000
    spike_counts_at_start = spike_count_at_start / total_seconds

    spike_counts_mean_start = spike_count_at_start.mean()
    spike_std_start = spike_count_at_start.std()

    spike_count_at_end = end_of_tone_trials.node_ids.value_counts()
    total_seconds = (1000)/1000
    spike_counts_at_end = spike_count_at_end / total_seconds

    spike_counts_mean_end = spike_count_at_end.mean()
    spike_std_end = spike_count_at_end.std()

    print("spike mean at start is {:.2f} with std of {:.2f}".format(spike_counts_mean_start,spike_std_start))
    print("spike mean at end is {:.2f} with std of {:.2f}".format(spike_counts_mean_end,spike_std_end))
    """
    fig, ax = plt.subplots(1,1, figsize=(12, 6),tight_layout=True)
    f = h5py.File(spike_path)
    spikes_df = pd.DataFrame(
        {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})
    start = 2000
    end = 2500
    for i in range(30):
        cell_spikes = spikes_df
        # skip the first few ms
        cell_spikes = cell_spikes[cell_spikes['timestamps'] > start]
        cell_spikes = cell_spikes[cell_spikes['timestamps'] < end]
        spike_counts = cell_spikes.node_ids.value_counts()

        spike_counts_per_second = spike_counts/0.5

        spikes_mean = spike_counts_per_second.mean()
        spikes_std = spike_counts_per_second.std()

        print("trial{} mean {:.2f} std {:.2f}".format(i,spikes_mean,spikes_std))

        start = start + 1500
        end = end + 1500

    if ax:
        ax.hist(spike_counts_per_second, bins=10, histtype='bar')
    if ax:
        #ax.set_xscale('log')
        ax.legend()
        ax.set_xlabel('Hz')
        ax.set_ylabel('amount of cells')
    #plt.show()

def synaptic_study(cell_ids,syn_path):
    file = h5py.File(syn_path, 'r')
    cai_trace = file['report']['BLA']['data']

    time_ds = file['report/BLA/mapping/time']
    tstart = time_ds[0]
    tstop = time_ds[1]
    #x_axis = np.linspace(tstart, tstop, len(cai_trace), endpoint=True)

    gids_ds = file['report/BLA/mapping/node_ids']
    index_ds = file['report/BLA/mapping/index_pointer']
    gids_ds = cell_ids
    index_lookup = {gids_ds[i]: (index_ds[i], index_ds[i+1]) for i in range(len(gids_ds))}
    tone_noise_data = []
    tone_trial_data = []
    #print(gids_ds[:])
    print("Looking at syn weight")
    for i in tqdm(range(len(gids_ds))):
        if(gids_ds[i] in tone_synapses):
            var_indx = index_lookup[gids_ds[i]][0]
            data = cai_trace[:,var_indx]
            tone_trial_data.append(data)
        else:
            var_indx = index_lookup[gids_ds[i]][0]
            data = cai_trace[:,var_indx]
            tone_noise_data.append(data)
    print("tone trial")
    compare_weight(tone_trial_data,start_time = 0,end_time=10000)
    print('tone noise')
    compare_weight(tone_noise_data,start_time = 0,end_time=10000)

def compare_weight(array, start_time, end_time, decay_over_10sec = 0.0046369585134881175, decay_weight=30,fudge_factor = 80):
    W = array
    weight_at_start = []
    weight_at_end = []

    for i in range(len(W)):
        weight_at_start.append(W[i][:(start_time*10)+1])
    for i in range(len(W)):
        weight_at_end.append(W[i][(end_time*10)-1:])
    lower_than_start_weight = 0
    higher_than_start_weight = 0
    decay_weight = 0
    for i in range(len(weight_at_start)):
        if ((weight_at_start[i] - weight_at_end[i]) * (decay_weight/weight_at_start[i]) < decay_over_10sec * fudge_factor
        and weight_at_start[i] > weight_at_end[i]):
            decay_weight = decay_weight + 1
        if ((weight_at_start[i] - weight_at_end[i]) * (decay_weight/weight_at_start[i]) > decay_over_10sec * fudge_factor
        and weight_at_start[i] > weight_at_end[i]):
            lower_than_start_weight = lower_than_start_weight + 1
        if ((weight_at_start[i] - weight_at_end[i]) * (decay_weight/weight_at_start[i]) > decay_over_10sec * fudge_factor
        and weight_at_start[i] < weight_at_end[i]):
            higher_than_start_weight = higher_than_start_weight + 1
    #print(weight_at_start[0] - weight_at_end[0])

    precent_higher = higher_than_start_weight/len(weight_at_start)*100
    precent_lower = lower_than_start_weight/len(weight_at_start)*100
    precent_decay = decay_weight/(len(weight_at_start))*100
    print("Number of synapses that decayed {} {:.2f}%".format(decay_weight,precent_decay))
    print("Number of synpases that entered LTP {} {:.2f}%".format(higher_than_start_weight,precent_higher))
    print("Number of synpases that entered LTD {} {:.2f}%".format(lower_than_start_weight,precent_lower))
    print("\n")

def tone_firing_rate(cell_ids,spike_path):
    f = h5py.File(spike_path)
    spikes_df = pd.DataFrame(
        {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})
    cell_spikes = spikes_df[spikes_df['node_ids'].isin(cell_ids)]
    all_trials = pd.DataFrame(columns=['node_ids', 'timestamps'])
    start = 500
    end = 1000
    time = 0
    for i in range(10):
        time = time + 500
        #print(start, end)
        cell_spikes_temp = cell_spikes[cell_spikes['timestamps'] > start]
        cell_spikes_temp = cell_spikes_temp[cell_spikes['timestamps'] < end]
        all_trials = all_trials.append(cell_spikes_temp)
        start = start + 1500
        end = end + 1500

    spike_counts = all_trials.node_ids.value_counts()
    total_seconds = (5000)/1000
    spike_counts = spike_counts / total_seconds

    spike_counts_mean = spike_counts.mean()
    spike_std = spike_counts.std()
    print(spike_counts_mean,spike_std)


#synaptic_study(random_PN_A_array,'outputECP_tone/tone2PN_A_W.h5')
#tone_trials_firing_rate_look_at(random_PN_A_array,'spikes.h5')
#tone_trials_firing_rate_look_at(random_PN_C_array,'outputECP_long/spikes.h5')

#spontaneous_firing_rate(random_PN_A_array,'outputECP_baseline_0.75/spikes.h5',skip_ms=5000)
#spontaneous_firing_rate(random_PN_C_array,'outputECP_baseline_0.75/spikes.h5',skip_ms=5000)
#spontaneous_firing_rate(random_PV_array,'outputECP_baseline_0.75/spikes.h5',skip_ms=5000)
#spontaneous_firing_rate(random_SOM_array,'outputECP_baseline_0.75/spikes.h5',skip_ms=5000)

#tone_firing_rate(random_PN_A_array,'outputECP_tone/spikes.h5')
#tone_firing_rate(random_PN_C_array,'outputECP_tone/spikes.h5')
#tone_firing_rate(random_PV_array,'outputECP_tone/spikes.h5')
#tone_firing_rate(random_SOM_array,'outputECP_tone/spikes.h5')


#tone_trials_firing_rate_look_at(random_PN_A_array,'outputECP_tone/spikes.h5')








def NMDA_AMPA(nmda_path,ampa_path,gids):
    f = h5py.File(ampa_path)
    data = f['report']['BLA']['data']
    gids_ds = f['report/BLA/mapping/node_ids']
    index_ds = f['report/BLA/mapping/index_pointer']
    index_lookup = {gids_ds[i]: (index_ds[i], index_ds[i+1]) for i in range(len(gids_ds))}
    gids = gids_ds.keys() if gids_ds is None else gids
    ampa_current_array = []
    for gid in gids:
        try:
            var_indx = index_lookup[gid][0]
            ampa_current = data[:,var_indx]
            ampa_current_array.append(sum(ampa_current))
        except:
            pass
            print('gid {} not in report'.format(gid))

    f = h5py.File(nmda_path)
    data = f['report']['BLA']['data']
    gids_ds = f['report/BLA/mapping/node_ids']
    index_ds = f['report/BLA/mapping/index_pointer']
    index_lookup = {gids_ds[i]: (index_ds[i], index_ds[i+1]) for i in range(len(gids_ds))}
    gids = gids_ds.keys() if gids_ds is None else gids
    nmda_current_array = []
    for gid in gids:
        try:
            var_indx = index_lookup[gid][0]
            nmda_current = data[:,var_indx]
            nmda_current_array.append(sum(nmda_current))
        except:
            pass
            print('gid {} not in report'.format(gid))
    return(ampa_current_array,nmda_current_array)
    

def gaba_current(gaba_path,gids):
    f = h5py.File(gaba_path)
    data = f['report']['BLA']['data']
    gids_ds = f['report/BLA/mapping/node_ids']
    index_ds = f['report/BLA/mapping/index_pointer']
    index_lookup = {gids_ds[i]: (index_ds[i], index_ds[i+1]) for i in range(len(gids_ds))}
    gids = gids_ds.keys() if gids_ds is None else gids
    gaba_current_array = []
    for gid in gids:
        try:
            var_indx = index_lookup[gid][0]
            gaba_current = data[:,var_indx]
            gaba_current_array.append(sum(gaba_current))
        except:
            pass
            print('gid {} not in report'.format(gid))
    return(gaba_current_array)


def find_firing_rate(spikes_df, gids, skip_ms, ms):
    cell_spikes = spikes_df[spikes_df['node_ids'].isin(gids)]
    cell_spikes = cell_spikes.sort_values('node_ids')
    cell_spikes = cell_spikes[cell_spikes['timestamps']>skip_ms]
    spike_counts = cell_spikes.node_ids.value_counts()
    total_seconds = (ms-skip_ms)/1000
    spike_counts_per_second = spike_counts / total_seconds
    spikes_mean = spike_counts_per_second.mean()
    return(spike_counts_per_second.sort_index())

#iampa = iampa[::100] #downsample
#f = h5py.File(nmda_path)
#inmda = sum(f['report']['BLA']['data'][:])
#inmda = inmda[::100] #downsample
#percent_NMDA = ((abs(inmda))/(abs(inmda) + abs(iampa)))
#print(sum(percent_NMDA)/len(percent_NMDA)*100)

f = h5py.File('outputECP_NMDA_0.5/spikes.h5')
spikes_df = pd.DataFrame({'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})
hz = find_firing_rate(spikes_df=spikes_df,gids=sorted(random_PN_A_array), skip_ms=5000, ms=10000)

tone2PN_ampa,tone2PN_nmda = NMDA_AMPA(nmda_path='outputECP_NMDA_0.5/tone2PN_A_inmda.h5',ampa_path='outputECP_NMDA_0.5/tone2PN_A_iampa.h5',gids=sorted(random_PN_A_array))
bg2PN_ampa,bg2PN_nmda = NMDA_AMPA(nmda_path='outputECP_NMDA_0.5/bg2PN_A_inmda.h5',ampa_path='outputECP_NMDA_0.5/bg2PN_A_iampa.h5',gids=sorted(random_PN_A_array))
PN2PN_ampa,PN2PN_nmda = NMDA_AMPA(nmda_path='outputECP_NMDA_0.5/PN2PN_A_inmda.h5',ampa_path='outputECP_NMDA_0.5/PN2PN_A_iampa.h5',gids=sorted(random_PN_A_array))
PV2PN_gaba = gaba_current(gaba_path='outputECP_NMDA_0.5/PV2PN_A_igaba.h5',gids=sorted(random_PN_A_array))
SOM2PN_gaba = gaba_current(gaba_path='outputECP_NMDA_0.5/SOM2PN_A_igaba.h5',gids=sorted(random_PN_A_array))

#tone2PN_ampa_block,tone2PN_nmda_block = NMDA_AMPA(nmda_path='outputECP_NMDA_0.5/tone2PN_A_inmda.h5',ampa_path='outputECP_NMDA_0.5/tone2PN_A_iampa.h5',gids=sorted(random_PN_A_array))
#bg2PN_ampa_block,bg2PN_nmda_block = NMDA_AMPA(nmda_path='outputECP_NMDA_0.5/bg2PN_A_inmda.h5',ampa_path='outputECP_NMDA_0.5/bg2PN_A_iampa.h5',gids=sorted(random_PN_A_array))
#PN2PN_ampa_block,PN2PN_nmda_block = NMDA_AMPA(nmda_path='outputECP_NMDA_0.5/PN2PN_A_inmda.h5',ampa_path='outputECP_NMDA_0.5/PN2PN_A_iampa.h5',gids=random_PN_A_array)

#for i in range(len(tone2PN_ampa)):
#    temp = ((tone2PN_ampa[i] - tone2PN_ampa_block[i])/abs(tone2PN_ampa[i]))*100
#    #print(temp)

#for i in range(len(bg2PN_ampa)):
#    temp = ((bg2PN_ampa[i] - bg2PN_ampa_block[i])/abs(bg2PN_ampa[i]))*100
#    print(temp)

#for i in range(len(PN2PN_ampa)):
#    temp = ((PN2PN_ampa[i] - PN2PN_ampa_block[i])/abs(PN2PN_ampa[i]))*100
#    print(temp)

df = pd.read_csv('connection table.csv')
df = df[df['cell id'].isin(random_PN_A_array)]
df['tone ampa'] = tone2PN_ampa
df['bg ampa'] = bg2PN_ampa
df['PN ampa'] = PN2PN_ampa
df['tone nmda'] = tone2PN_nmda
df['bg nmda'] = bg2PN_nmda
df['PN nmda'] = PN2PN_nmda
df['PV gaba'] = PV2PN_gaba
df['SOM gaba'] = SOM2PN_gaba
df['Hz'] = hz
df.to_csv('AMPA NMDA table.csv')
















