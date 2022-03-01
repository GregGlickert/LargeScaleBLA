import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from bmtk.analyzer.compartment import plot_traces

tone2pyr = 'network/tone_BLA_edges.h5'
tone = h5py.File(tone2pyr,'r')
#print(tone['edges']['tone_to_BLA']['target_node_id'][:1000])
def get_array(path):
    try:
        array = h5py.File(path,'r')
        array = (array['report']['BLA']['data'][:])
    except:
        pass
    return array

def generate_plot(trials,box_low, box_height, title_name, path1, path2):
    file1 = path1
    file2 = path2
    weight = get_array(file1)
    cai = get_array(file2)
    fig, axs = plt.subplots(1, 2, figsize=(18, 6))
    axs[0].plot(weight)
    axs[1].plot(cai)
    for i in range(trials):
        offset = i*40000 + 2000
        left1,bottom1,width1,height1 = (4000+offset,box_low,1000,box_height)
        left3, bottom3, width3, height3 = (0 + offset, box_low, 4000, box_height)
        left2, bottom2, width2, height2 = (4000 + offset, 0.00005, 1000, 0.0008)
        left4, bottom4, width4, height4 = (0 + offset, 0.00005, 4000, 0.0008)
        rect1 = mpatches.Rectangle((left1,bottom1),width1,height1, alpha=0.4,color='purple')
        rect3 = mpatches.Rectangle((left3,bottom3),width3,height3, alpha=0.4,color='orange')
        rect2 = mpatches.Rectangle((left2, bottom2), width2, height2, alpha=0.4, color='purple')
        rect4 = mpatches.Rectangle((left4, bottom4), width4, height4, alpha=0.4, color='orange')
        axs[0].text(6000 + offset, box_low + 3, 'tone + shock', fontsize=12, color='purple')
        axs[0].text(6000 + offset, box_low + 3.5, 'tone', fontsize=12, color='orange')
        axs[0].add_patch(rect1)
        axs[0].add_patch(rect3)
        axs[1].text(6000+offset, 0.0004, 'tone + shock', fontsize=12)
        axs[1].add_patch(rect2)
        axs[1].text(6000 + offset, 0.0004, 'tone + shock', fontsize=12, color='purple')
        axs[1].text(6000 + offset, 0.0005, 'tone', fontsize=12,  color='orange')
        axs[1].add_patch(rect4)
    axs[0].set_title('synaptic weight')
    axs[1].set_title('cai')
    fig.suptitle(title_name, fontsize=16)
    plt.show()


trials = 2
#tone2PN
#generate_plot(trials, 15, 1, path1= 'outputECP/syns_tone2pyr_should_change.h5', path2= 'outputECP/syns_tone2pyr_should_change_cai.h5', title_name='tone2pn')

#plot_traces(report_path='outputECP/v_report.h5',node_ids=[955])

#pn2pn
#generate_plot(trials,3, 5, path1='outputECP/syns_pyr2pyr_should_not_change.h5', path2='outputECP/syns_pyr2pyr_should_not_change_cai.h5', title_name='pn2pn')

#pn2int
#generate_plot(trials,3, 15, path1='outputECP/syns_pyrD2interD_STFD_should_change.h5', path2='outputECP/syns_pyrD2interD_STFD_should_change_cai.h5', title_name='pn2int changing')

generate_plot(trials,3, 15, path1='outputECP/syns_pyrD2interD_STFD_should_not_change.h5', path2='outputECP/syns_pyrD2interD_STFD_should_not_change_cai.h5', title_name='pn2int not changing')

#int2pn
generate_plot(trials,5, 20, path1='outputECP/syns_interD2pyrD_STFD_should_change.h5', path2='outputECP/syns_interD2pyrD_STFD_should_change_cai.h5', title_name='int2pn changing')

generate_plot(trials,5, 20, path1='outputECP/syns_interD2pyrD_STFD_should_not_change.h5', path2='outputECP/syns_interD2pyrD_STFD_should_not_change_cai.h5', title_name='int2pn not changing')

#tone2INT
#generate_plot(trials,3, 1, path1='outputECP/syns_tone2interD_should_change.h5', path2='outputECP/syns_tone2interD_should_change_cai.h5', title_name='tone2int changing')

#generate_plot(trials,3, 1, path1='outputECP/syns_tone2interD_should_not_change.h5', path2='outputECP/syns_tone2interD_should_not_change_cai.h5', title_name='tone2int changing')

