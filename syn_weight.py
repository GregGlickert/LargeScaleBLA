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

path_PN2PN = "outputECP/syns_pyrD2interD_STFD_should_change.h5"

PN2PN = get_array(path_PN2PN)
plt.plot(PN2PN)
plt.show()