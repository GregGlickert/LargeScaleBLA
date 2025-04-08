import h5py
import matplotlib.pyplot as plt
from bmtk.analyzer.compartment import plot_traces
from bmtk.utils.reports.compartment import CompartmentReport
import numpy as np


def get_array(path):
    try:
        array = h5py.File(path,'r')
        array = (array['report']['BLA']['data'][:])
    except:
        pass
    return array

def check_thresholds(path,node,threshold1,threshold2):
    report = CompartmentReport(path)
    data = report.data(node_id=node)
    above_1 = np.sum(data>threshold1)
    above_2 = np.sum(data>threshold2)   
    return(above_1,above_2)


path = 'outputECP_baseline/tone2PN_cai.h5'
check_the_thresholds = False
if check_the_thresholds == True:
    above_thres_1 = []
    above_thres_2 = []
    for i in range(800):
        above1,above2 = check_thresholds(path,node=i,threshold1=1,threshold2=2)
        above_thres_1.append(above1)
        above_thres_2.append(above2)

cai = get_array(path)
cai2 = get_array(path)
plt.figure(1)
plt.plot(cai)
plt.ylim(0.6,1.1)
plt.figure(2)
plt.plot(cai2)
plt.ylim(1.1,2)

#plot_traces(report_path = 'outputECP_tone+shock/tone2PN_cai.h5')
plt.show()