"""
A python implementation of matlab/analysis.m

TB - 8/4/21
"""

from scipy.signal import hanning,welch,decimate
import h5py
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

scale = 1

def raster(spikes_df,node_set,skip_ms=0,ax=None):
    spikes_df = spikes_df[spikes_df['timestamps']>skip_ms] 
    for node in node_set:
        cells = range(node['start'],node['end']+1) #+1 to be inclusive of last cell
        cell_spikes = spikes_df[spikes_df['node_ids'].isin(cells)]

        ax.scatter(cell_spikes['timestamps'],cell_spikes['node_ids'],
                   c='tab:'+node['color'],s=3, label=node['name'])
    
    handles,labels = ax.get_legend_handles_labels()
    ax.legend(reversed(handles), reversed(labels))
    ax.grid(False)


def spike_frequency_bar_graph(spikes_df, node_set, ms, start=0, end=15000, ax=None, n_bins=10):
    mean = []
    name = []
    labels = []
    for node in node_set:
        cells = range(node['start'], node['end'] + 1)  # +1 to be inclusive of last cell
        cell_spikes = spikes_df[spikes_df['node_ids'].isin(cells)]

        # skip the first few ms
        cell_spikes = cell_spikes[cell_spikes['timestamps'] > start]
        cell_spikes = cell_spikes[cell_spikes['timestamps'] < end]
        spike_counts = cell_spikes.node_ids.value_counts()
        total_seconds = (ms) / 1000
        spike_counts_per_second = spike_counts / total_seconds

        spikes_mean = spike_counts_per_second.mean()
        spikes_std = spike_counts_per_second.std()

        label = "{} : {:.2f} ({:.2f})".format(node['name'], spikes_mean, spikes_std)
        # print(label)
        c = "tab:" + node['color']
        if ax:
            mean.append(spikes_mean)
            name.append(node['name'])
            labels.append(label)
            ax.bar(node['name'], spikes_mean, label=label, color=c)

    if ax:
        ax.legend()
        
        

def run(show_plots=False,save_plots=False):
    

    dt = 0.05
    steps_per_ms = 1/dt
    skip_seconds = 5
    skip_ms = skip_seconds*1000
    skip_n = int(skip_ms * steps_per_ms)
    end_ms = 15000

    spikes_location = 'outputECP/spikes.h5'

    print("loading " + spikes_location)
    f = h5py.File(spikes_location)
    spikes_df = pd.DataFrame({'node_ids':f['spikes']['BLA']['node_ids'],'timestamps':f['spikes']['BLA']['timestamps']})
    print("done")


    node_set = [
        {"name":"PN","start":0*scale,"end":799*scale,"color":"blue"},
        {"name":"PV","start":800*scale,"end":892*scale,"color":"red"},
        {"name":"SOM","start":893*scale,"end":943*scale,"color":"green"},
        {"name":"CR","start":944*scale,"end":999*scale,"color":"purple"}
    ]
    
    if show_plots or save_plots:
        print("plotting...")
        fig, (ax1, ax2) = plt.subplots(1,3,figsize=(15,4.8))#6.4,4.8 default
        fig.suptitle('Amygdala Theta Analysis')
        start1 = 0
        end1 = 15000
        spike_frequency_bar_graph(spikes_df,node_set,
                                  start=start1,end=end1,ax=ax2,ms=(end1-start1))
        raster(spikes_df,node_set,skip_ms=skip_ms,ax=ax1)
        if save_plots:
            f_name = 'analysis.png'
            print("saving " + f_name)
            plt.savefig(f_name, bbox_inches='tight')
        if show_plots:
            print("showing plots...")
            fig.tight_layout()
            plt.show()
         
    else:
        pass


if __name__ == '__main__':
    show_plots = False
    save_plots = False
    if '--show-plots' in sys.argv:
        show_plots = True
    if '--save-plots' in sys.argv:
        save_plots = True
        
    run(show_plots=show_plots, save_plots=save_plots)
