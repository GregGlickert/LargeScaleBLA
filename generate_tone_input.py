import string
import h5py
import pandas as pd
import csv
import numpy as np
from bmtk.utils.reports.spike_trains import PoissonSpikeGenerator
import random

random.seed(123412)
np.random.seed(123412)
tone_synapses = random.sample(range(4000), 2800) # 70% of cells get a tone_synapses
tone_synapses.sort()
#print(tone_synapses)

def poisson_array(time,node_id):
    #generates poisson input for given time and node id and returns spiketrain in form of timestamps
    psg = PoissonSpikeGenerator(population='tone')
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

def generate_tone_input(baseline_case =  True):
    whole_signal = []
    print("building tone input baseline")
    if baseline_case == False:
        print("With tone trials!")
    for i in range(4000):
        node_id = i
        if i < 3572:
            p_array = poisson_array(20,node_id)
            noise_array = []
            for i in range(len(p_array)):
                noise_array.append((p_array[i]).astype(str) + str(" 'tone' ") + str(node_id))
        #print(noise_array)
        if baseline_case == False:
            time = 3000 # let cells rest for 5000ms then start trials
            if node_id in tone_synapses:
                for i in range(0,30): # number of trials
                    trial_array = tone_trial(tstart = time, node_id=node_id)
                    time = time + 1500 #gap between trial starts
                    whole_signal.append(trial_array) # comment out to generate baseline case
        whole_signal.append(noise_array)
    whole_signal = flatten(whole_signal)
    d = {'timestamps population node_ids' : whole_signal}
    df = pd.DataFrame(data=d)
    if baseline_case ==  True:
        df.to_csv("tone_spikes_baseline.csv",index=False)
    if baseline_case == False:
        df.to_csv("tone_spikes_trials.csv",index=False)
        


generate_tone_input()




    
    

