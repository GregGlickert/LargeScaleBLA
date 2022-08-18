import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from bmtk.analyzer.compartment import plot_traces


def get_array(path):
    try:
        array = h5py.File(path,'r')
        array = (array['report']['BLA']['data'][:])
    except:
        pass
    return array

path_tone2PN = "outputECP/tone2pyr.h5"

tone = get_array(path_tone2PN)
plt.plot(tone)
plt.show()

path_tone2PN = "outputECP/tone2pyr_cai.h5"

tone = get_array(path_tone2PN)
tone[:] = [x * 1000 for x in tone]
plt.plot(tone)
plt.show()

