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

path = 'outputECP/v_report.h5'

voltage_array = get_array(path)

plt.plot(voltage_array)
plt.show()
