import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from bmtk.analyzer.compartment import plot_traces

tone2pyr = 'network/tone_BLA_edges.h5'
tone = h5py.File(tone2pyr,'r')
#print(tone['edges']['tone_to_BLA']['target_node_id'][:600])

def get_array(path):
    try:
        array = h5py.File(path,'r')
        array = (array['report']['BLA']['data'][:])
    except:
        pass
    return array
file1 = 'outputECP/syns_tone2pyr.h5'
file2 = 'outputECP/syns_cai.h5'

weight = get_array(file1)
cai = get_array(file2)
fig, axs = plt.subplots(1, 2, figsize=(15, 6))
axs[0].plot(weight)
axs[1].plot(cai)
trials = 4
for i in range(trials):
    offset = i*40000
    left1,bottom1,width1,height1 = (4000+offset,7,1000,3)
    left2, bottom2, width2, height2 = (4000 + offset, 0.00005, 1000, 0.0004)
    rect1 = mpatches.Rectangle((left1,bottom1),width1,height1, alpha=0.2,color='purple')
    rect2 = mpatches.Rectangle((left2, bottom2), width2, height2, alpha=0.2, color='purple')
    axs[0].text(6000+offset, 7.5, 'tone + shock', fontsize=12)
    axs[0].add_patch(rect1)
    axs[1].text(6000+offset, 0.0004, 'tone + shock', fontsize=12)
    axs[1].add_patch(rect2)
axs[0].set_title('synaptic weight')
axs[1].set_title('cai')
fig.suptitle('Tone2PN synapse', fontsize=16)
plt.show()

#v = plot_traces('simulation_config_ts.json')