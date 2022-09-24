import pandas as pd
import h5py
import numpy as np
import matplotlib.pyplot as plt
import math

f = h5py.File('outputECP/spikes.h5')
spikes_df = pd.DataFrame({'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})

def get_PSTH(node_id,df):
    timestamp = 0
    df0 = df.loc[df['node_ids'] == node_id]
    df0.sort_values(by=['timestamps'])
    x0 = df0['timestamps'].tolist()
    trial_spikes = []
    i = 0
    while(i < 10):
        for j in range(len(x0)):
            if(x0[j] >= timestamp+(i*3500) and x0[j] <= timestamp+(i*3500+1500)):
                value = (x0[j]-(i*3500) - timestamp)
                value = value/1000
                value = value - 0.5
                trial_spikes.append(value)
        i = i+1
    return(trial_spikes)

def find_bins(array, width):
    try:
        minimmum = np.min(array)
        maximmum = np.max(array)
        bound_min = -1.0 * (minimmum % width - minimmum)
        bound_max = maximmum - maximmum % width + width
        n = int((bound_max - bound_min) / width) + 1
        bins = np.linspace(bound_min, bound_max, n)
    except:
        bins = 10
    return bins

array = get_PSTH(3300,spikes_df)  # PN 2753, PV 3300

bins = find_bins(array,0.01)



plt.hist(array,bins)
plt.ylabel("spikes during tone summed")
plt.xlabel("time")
plt.xlim(-0.5,1)
plt.title("PSTH")
plt.show()