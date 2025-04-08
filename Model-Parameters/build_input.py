import numpy as np
import pandas as pd
import h5py
import shutil
import random
import os
# BMTK changed how the PoissonSpikeGenerator works for literally no reason. Instead of fixing it i copied the old one and use it
from bmtk.utils.reports.spike_trains import PoissonSpikeGenerator as P_spike_generator 
from spike_trains_original import PoissonSpikeGenerator

random.seed(123412)
np.random.seed(123412)

INPUT_PATH = "./-10input"

try:
    shutil.rmtree(INPUT_PATH)
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

def build_input(t_sim, numPN_A = 569, numPN_C=231, numPV = 93, numSOM=51,scale=None):
    
    # THALAMUS
    population = 'thalamus_pyr'
    build_poisson_input(population=population,
                        node_ids=range((numPN_A+numPN_C)*scale),
                        mean=2,std=1,
                        output_h5= os.path.join(INPUT_PATH,population+".h5"),
                        t_sim=t_sim)

    population = 'thalamus_pv'
    build_poisson_input(population=population,
                        node_ids=range((numPV)*scale),
                        mean=2,std=1,
                        output_h5= os.path.join(INPUT_PATH,population+".h5"),
                        t_sim=t_sim)
    population = 'thalamus_som'
    build_poisson_input(population=population,
                    node_ids=range((numSOM)*scale),
                    mean=2,std=1,
                    output_h5= os.path.join(INPUT_PATH,population+".h5"),
                    t_sim=t_sim)
    population = 'thalamus_vip'
    build_poisson_input(population=population,
                    node_ids=range((numSOM)*scale),
                    mean=2,std=1,
                    output_h5= os.path.join(INPUT_PATH,population+".h5"),
                    t_sim=t_sim)

# Tone generation stuff
def poisson_array(time,node_id):
    #generates poisson input for given time and node id and returns spiketrain in form of timestamps
    psg = P_spike_generator(population='tone')
    POISSON_PATH = 'poisson.h5'
    POISSON_PATH = os.path.join(INPUT_PATH,POISSON_PATH)
    psg.add(node_ids=node_id,firing_rate=2,times=(0.0, time))  
    psg.to_sonata(POISSON_PATH)

    f = h5py.File(POISSON_PATH)
    return (f['spikes']['tone']['timestamps'][:])
    f.close()

def tone_trial_csv(tstart, node_id):
    tone_array = []
    for i in range(0, 505, 50): # 20 hz rn
        tone_array.append(str(tstart + i) + str(' tone ') + str(node_id))
    return(tone_array)

def tone_trial(tstart, node_id):
    node_ids = []
    timestamps = []
    for i in range(0, 505, 50): # 20 hz rn
        node_ids.append(node_id)
        timestamps.append(tstart+i)
    return(node_ids,timestamps)

def flatten(l):
    return [item for sublist in l for item in sublist]

def generate_tone_input_csv(with_tone_trials = None, scale = None,sim_time = None,num_tone_trials= None,trial_start = None):
    whole_signal = []
    cell_count = scale * 1000
    tone_synapses = random.sample(range(cell_count), int(cell_count*0.7)) # 70% of cells get a tone_synapses
    tone_synapses.sort()
    if with_tone_trials == False:
        print("building tone input noise at 2Hz!")
    if with_tone_trials == True:
        print("building tone input noise at 2Hz! for trials dataset")
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
        df.to_csv(os.path.join(INPUT_PATH,'tone_spikes_baseline.csv'),index=False)
    if with_tone_trials == True:
        df.to_csv(os.path.join(INPUT_PATH,'tone_spikes_trials.csv'),index=False)

def generate_tone_input(with_tone_trials = None, scale = None,sim_time = None,num_tone_trials= None,trial_start = None,tone_gap = None,tone_synapses=None):
    whole_signal = []
    node_ids = []
    timestamps = []
    if with_tone_trials == False:
        print("building tone input noise at 2Hz!")
    if with_tone_trials == True:
        print("building tone input noise at 2Hz! for trials dataset")
        print("There are " + str(num_tone_trials) + " trials and they start at " + str(trial_start) + " ms")
    for i in range(cell_count):
        node_id = i
        if i < (800+93)*scale: # amount of PN and PV cells
            p_array = poisson_array(sim_time,node_id)
            noise_array = []
            for i in range(len(p_array)):
                noise_array.append((p_array[i]).astype(str) + str(" 'tone' ") + str(node_id))
                node_ids.append(node_id)
                timestamps.append(p_array[i])
        #print(noise_array)
        if with_tone_trials == True:
            time = trial_start # let cells rest then start trials
            if node_id in tone_synapses:
                for i in range(0,num_tone_trials): # number of trials
                    node_ids_temp, timestamps_temp = tone_trial(tstart = time, node_id=node_id)
                    #print(time)
                    time = time + tone_gap #gap between trial starts
                    node_ids.extend(node_ids_temp)
                    timestamps.extend(timestamps_temp)
   

    if with_tone_trials ==  False:
        out = os.path.join(INPUT_PATH,'tone_spikes_baseline.h5')
        tone = h5py.File(out, 'w')

        tone_spikes = tone.create_group("spikes")
        final_tone = tone_spikes.create_group("tone")

        final_tone.create_dataset("node_ids", data=node_ids)
        final_tone.create_dataset("timestamps", data=timestamps)
        tone.close()

    if with_tone_trials == True:
        out = os.path.join(INPUT_PATH,'tone_spikes_trials.h5')
        tone = h5py.File(out, 'w')

        tone_spikes = tone.create_group("spikes")
        final_tone = tone_spikes.create_group("tone")

        final_tone.create_dataset("node_ids", data=node_ids)
        final_tone.create_dataset("timestamps", data=timestamps)
        tone.close()
    
def shock_trials(tstart):
    shock_array = []
    for i in range(0, 105, 25):
        #shock_array.append(str(tstart + i) + str(" 'shock' 0"))
        shock_array.append(tstart+i)
    return shock_array
        
def generate_shock(time, node_id):
    psg = P_spike_generator(population="shock")
    SHOCK_PATH = 'shocks.h5'
    for i in range(len(time)):
        time[i] = time[i]/1000
    psg.add(node_ids=node_id,firing_rate=150,times=(time))  
    psg.to_sonata(os.path.join(INPUT_PATH,SHOCK_PATH))

    f = h5py.File(os.path.join(INPUT_PATH,SHOCK_PATH))
    return ((f['spikes']['shock']['timestamps'][:]),f['spikes/shock/node_ids'][:])

def write_shock(trial_start,num_tone_trials,scale = None,tone_gap = None):
    print("generating shock input")
    SHOCK_PATH = 'shocks.csv'
    tshock = trial_start + 400 # was 400
    whole_signal = []
    network_scale = scale * 1000
    interneuron_range = (int(network_scale*(0.8)), network_scale)
    #print(interneuron_range)
    for i in range(0,num_tone_trials): # number of trials
        shock_array = []
        trial_array = shock_trials(tshock)
        #print(tshock)
        tshock = tshock + tone_gap #gap between trial starts
        pos_input, node_id = generate_shock(time=trial_array,node_id=range(0,10000))
        for i in range(len(pos_input)):
                shock_array.append((pos_input[i]).astype(str) + str(" 'shock' ") + str(node_id[i]))
        whole_signal.append(shock_array)
    whole_signal = flatten(whole_signal)
    #print(whole_signal)
    d = {'timestamps population node_ids' : whole_signal}
    df = pd.DataFrame(data=d)
    df.to_csv(os.path.join(INPUT_PATH,SHOCK_PATH),index=False)

                             
network_scale = 1 #5
simulation_time_in_secs = 300  #47
# full expierment should take 36.5 seconds
print("T_sim is set to " + str(simulation_time_in_secs) + " seconds")
print("The network scale is set to " +str(network_scale))

cell_count = network_scale * (800+93) #PN and PV cell amount
cell_list = list(range(0,cell_count))
random.shuffle(cell_list)
size = len(cell_list)
CS1_70 = cell_list[int(size*0.3):] # slices 30% off = 70% of cells getting tone
CS1 = cell_list[int(size*0.5):] #50%
CS5 = cell_list[:int(size*0.5)] #50%

CS2 = CS1[int((len(CS1))*0.75):] + CS5[int((len(CS1))*0.25):]
CS3 = CS1[int((len(CS1))*0.5):] + CS5[int((len(CS1))*0.5):]
CS4 = CS1[int((len(CS1))*0.25):] + CS5[int((len(CS1))*0.75):]

#to make sure array is correct size
CS2 = CS2[:int(size/2)]
CS3 = CS3[:int(size/2)]
CS4 = CS4[:int(size/2)]
#CS5 = CS5[:int(size/2)]


build_input(simulation_time_in_secs, scale=network_scale)

generate_tone_input(with_tone_trials=False, scale=network_scale,sim_time=simulation_time_in_secs,
                    num_tone_trials=30, trial_start=5000,tone_gap=1500,tone_synapses=CS1_70)

generate_tone_input(with_tone_trials=True, scale=network_scale,sim_time=simulation_time_in_secs,
                    num_tone_trials=30, trial_start=5000,tone_gap=1500,tone_synapses=CS1_70) #5000


write_shock(trial_start=12500,num_tone_trials=16,scale=network_scale,tone_gap=1500) #20000 12500
