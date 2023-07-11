import h5py
import matplotlib.pyplot as plt
from bmtk.analyzer.compartment import plot_traces

plot_traces(report_path = 'outputECP_lowerthres2_lowlearn_5000/v_report.h5',node_ids=[4000])
plt.show()