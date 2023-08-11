from bmtk.analyzer.compartment import plot_traces
from bmtk.utils.reports.compartment import CompartmentReport
import matplotlib.pyplot as plt
import h5py

"""
nodes = [910,911,912,913,914,915,916,917,918,919,920,921,922,923,924]

for i in range (len(nodes)):
    plt.figure(i)
    plot_traces(report_path = 'outputECP_tone+shock/v_report.h5',node_ids=nodes[i],show=False)

plt.show()
"""

voltage = CompartmentReport(path='outputECP_tone+shock/v_report.h5')
cell_voltage = voltage.data(node_id=1)
plt.plot(cell_voltage)
plt.show()



    