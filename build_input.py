import numpy as np
import pandas as pd
import h5py
import shutil
import random
# BMTK changed how the PoissonSpikeGenerator works for literally no reason. Instead of fixing it i copied the old one and use it
from bmtk.utils.reports.spike_trains import PoissonSpikeGenerator as P_spike_generator 
from spike_trains_original import PoissonSpikeGenerator

random.seed(123412)
np.random.seed(123412)

try:
    shutil.rmtree("inputs")
    print("deleted old inputs!")
except:
    pass

def lognorm_fr_list(n,m,s):
    mean = np.log(m) - 0.5 * np.log((s/m)**2+1)
    std = np.sqrt(np.log((s/m)**2 + 1))
    return [np.random.lognormal(mean,std) for i in range(n)]

def build_poisson_input(population,node_ids,mean,std,output_h5,t_sim=None):
    print('Building input for ' + population + "[" + str(len(node_ids)) + " cells at " + str(mean) + "(" + str(std) + ") Hz]")
    psg = PoissonSpikeGenerator(population=population)
    psg.add(node_ids=node_ids,  
    firing_rate=lognorm_fr_list(len(node_ids),mean,std),
    times=(0.0, t_sim))  
    psg.to_sonata(output_h5)

def build_input(t_sim, numPN_A = 569, numPN_C=231, numPV = 100, numSOM=100,scale=None):
    
# THALAMUS
    build_poisson_input(population='thalamus_pyr_A',
                        node_ids=range((numPN_A)*scale),
                        mean=2,std=1,
                        output_h5='inputs/thalamus_pyr_A_spikes.h5',
                        t_sim=t_sim)

    build_poisson_input(population='thalamus_pyr_C',
                        node_ids=range((numPN_C)*scale),
                        mean=2,std=1,
                        output_h5='inputs/thalamus_pyr_C_spikes.h5',
                        t_sim=t_sim)
    
    # THALAMUS
    build_poisson_input(population='thalamus_pv',
                        node_ids=range((numPV)*scale),
                        mean=2,std=1,
                        output_h5='inputs/thalamus_pv_spikes.h5',
                        t_sim=t_sim)

    build_poisson_input(population='thalamus_som',
                    node_ids=range((numSOM)*scale),
                    mean=2,std=1,
                    output_h5='inputs/thalamus_som_spikes.h5',
                    t_sim=t_sim)

    build_poisson_input(population='thalamus_vip',
                    node_ids=range((numSOM)*scale),
                    mean=2,std=1,
                    output_h5='inputs/thalamus_vip_spikes.h5',
                    t_sim=t_sim)

# Tone generation stuff
def poisson_array(time,node_id):
    #generates poisson input for given time and node id and returns spiketrain in form of timestamps
    psg = P_spike_generator(population='tone')
    psg.add(node_ids=node_id,firing_rate=2,times=(0.0, time))  
    psg.to_sonata('poisson.h5')

    f = h5py.File('poisson.h5')
    return (f['spikes']['tone']['timestamps'][:])
    f.close()

def tone_trial(tstart, node_id):
    tone_array = []
    for i in range(0, 505, 50): # 20 hz rn
        tone_array.append(str(tstart + i) + str(' tone ') + str(node_id))
    return(tone_array)

def flatten(l):
    return [item for sublist in l for item in sublist]

def generate_tone_input(with_tone_trials = None, scale = None,sim_time = None,num_tone_trials= None,trial_start = None):
    whole_signal = []
    cell_count = scale * 1000
    tone_synapses = random.sample(range(cell_count), int(cell_count*0.7)) # 70% of cells get a tone_synapses
    tone_synapses.sort()
    if with_tone_trials == False:
        print("building tone input noie at 2Hz!")
    if with_tone_trials == True:
        print("building tone input noie at 2Hz! for trials dataset")
        print("There are " + str(num_tone_trials) + " trials and they start at " + str(trial_start) + " ms")
    for i in range(cell_count):
        node_id = i
        if i < 900*scale: # amount of PN and PV cells
            p_array = poisson_array(sim_time,node_id)
            noise_array = []
            for i in range(len(p_array)):
                noise_array.append((p_array[i]).astype(str) + str(" 'tone' ") + str(node_id))
        #print(noise_array)
        if with_tone_trials == True:
            time = trial_start # let cells rest then start trials
            if node_id in tone_synapses:
                for i in range(0,num_tone_trials): # number of trials
                    trial_array = tone_trial(tstart = time, node_id=node_id)
                    time = time + 1500 #gap between trial starts
                    whole_signal.append(trial_array) # comment out to generate baseline case
        whole_signal.append(noise_array)
    whole_signal = flatten(whole_signal)
    d = {'timestamps population node_ids' : whole_signal}
    df = pd.DataFrame(data=d)
    if with_tone_trials ==  False:
        df.to_csv("inputs/tone_spikes_baseline.csv",index=False)
    if with_tone_trials == True:
        df.to_csv("inputs/tone_spikes_trials.csv",index=False)

network_scale = 10
simulation_time_in_secs = 47
print("T_sim is set to " + str(simulation_time_in_secs) + " seconds")
print("The network scale is set to " +str(network_scale))
build_input(simulation_time_in_secs, scale=network_scale)

generate_tone_input(with_tone_trials=False, scale=network_scale,sim_time=simulation_time_in_secs,
                    num_tone_trials=30, trial_start=3000)

generate_tone_input(with_tone_trials=True, scale=network_scale,sim_time=simulation_time_in_secs,
                    num_tone_trials=30, trial_start=3000)
