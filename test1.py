from bmtk.analyzer.compartment import plot_traces
from bmtk.analyzer.spike_trains import plot_raster
import matplotlib.pylab as plt
import h5py

_ = plot_traces(report_path='outputECP/v_report.h5',node_ids=[0,1,2,3,4,5], report_name='v_report',show=False)

#plot_raster(spikes_file='outputECP/spikes.h5')
#plt.show()

#data = h5py.File("outputECP/pyr2pyr.h5")
#print(data['report']['BLA']['data'][:])