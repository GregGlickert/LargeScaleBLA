import h5py
import matplotlib.pyplot as plt
from bmtk.analyzer.compartment import plot_traces


def get_array(path):
    try:
        array = h5py.File(path,'r')
        array = (array['report']['BLA']['data'][:])
    except:
        pass
    return array

#array = get_array("output_trials/shock2int.h5")
array = get_array("output_trials/tone2PN_cai.h5")
#array = get_array("output_trials/tone2PN.h5")
plt.plot(array)
plt.show()

#array = get_array("output_tone_shock/tone2PN.h5")
#plt.plot(array)
#plt.show()

#plot_traces(report_path="output_trials/tone2PN_cai.h5")

#f = h5py.File("inputs/shocks.h5")
#print(f['spikes/shock/node_ids'][:50])
#print(f['spikes/shock/timestamps'][:50])