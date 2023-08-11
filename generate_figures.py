from bmtool import bmplot
import h5py
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D
from bmtool.util import util
from bmtool.singlecell import Profiler
import statistics


from bmtool import bmplot
import h5py
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D
from bmtool.util import util
from bmtool.singlecell import Profiler
import statistics
import pandas as pd

def d_plot():
        populations_list = 'all'
        config = "simulation_configECP_base_homogenous.json"
        group_keys = 'pop_name'
        title = "test"
        save_file = "test.png"

        nodes = util.load_nodes_from_config(config)
        fig = plt.figure(figsize=(10,10))
        ax = fig.add_subplot(projection='3d') #changed from repo
        #handles = []

        test = pd.DataFrame.from_dict(nodes['BLA'])

        scale = 1
        node_set_split = [
            {"name": "PN", "start": 0 * scale, "end": 799 * scale, "color": "red"},
            {"name": "PV", "start": 800 * scale, "end": 899 * scale, "color": "blue"},
            {"name": "SOM", "start": 899 * scale, "end": 999 * scale, "color": "black"}
            #{"name": "VIP", "start": 1000 * scale, "end": 1106 * scale + 3, "color": "brown"}
        ]


        handles = []
        for cell in node_set_split:
            label = "{}".format(cell['name'])
            cells = range(cell['start'], cell['end'] + 1)  # +1 to be inclusive of last cell
            color = cell['color']
            nodes = test[test.index > cell["start"]]
            nodes = nodes[nodes.index < cell["end"]]
            h = ax.scatter(nodes['pos_x'],nodes['pos_y'],nodes['pos_z'],color=color,label=label)
            handles.append(h)
        #if not handles:
            #return
        plt.title(title)
        plt.legend(handles=handles)

        plt.draw()
        #plt.show()

        plt.savefig("3d plot.svg", format = 'svg', dpi=300)

def plot_current_inject(Cell,inj_amp,inj_delay,inj_dur):
    profiler = Profiler(template_dir='components/templates', 
                        mechanism_dir='components/mechanisms')
    
    time_vec, voltage_vec = profiler.current_injection(Cell,#post_init_function="insert_mechs(123)", 
                                                    inj_amp=inj_amp,inj_delay=inj_delay,inj_dur=inj_dur)

def plot_firing_rate_distro(spikes_df,node_set,ms,skip_ms=0,n_bins=20, graph = None):
    scale = 5
    node_set_split = [
        {"name": "PN_A", "start": 0 * scale, "end": 568 * scale , "color": "blue"},
        {"name": "PN_C", "start": 569 * scale, "end": 799 * scale, "color": "olive"},
        #{"name": "PN", "start": 0 * scale, "end": 799 * scale, "color": "olive"},
        {"name": "PV", "start": 800 * scale, "end": 899 * scale, "color": "purple"},
        {"name": "SOM", "start": 899 * scale, "end": 999 * scale, "color": "green"}
    ]
    
    fig, axs = plt.subplots(1,1, figsize=(12, 6),tight_layout=True)
    
    for node in node_set:
        if node['name'] != graph:
            pass
        else:
            total_seconds = (ms-skip_ms)/1000

            cells = range(node['start'],node['end']+1) #+1 to be inclusive of last cell
            cell_spikes = spikes_df[spikes_df['node_ids'].isin(cells)]

            #skip the first few ms
            cell_spikes = cell_spikes[cell_spikes['timestamps']>skip_ms]
            spike_counts = cell_spikes.node_ids.value_counts()
            total_seconds = (ms-skip_ms)/1000
            spike_counts_per_second = spike_counts / total_seconds

            spikes_mean = spike_counts_per_second.mean()
            spikes_std = spike_counts_per_second.std()
            spike_median = statistics.median(spike_counts_per_second)

            label = "{} : mean {:.2f} std ({:.2f}) median {:.2f}".format(node['name'],spikes_mean,spikes_std,spike_median)
            print(label)
            c = node['color']
            #ax.hist(spike_counts_per_second,n_bins,density=True,histtype='bar',label=label,color=c)
            axs.hist(spike_counts_per_second, label=label, color=c)
            locs = axs.get_yticks()
            axs.margins(0.5, 0.5)
            axs.legend()


d_plot()

#plot_current_inject(Cell='PN_A', inj_amp=300,inj_dur=500,inj_delay=100)
#plot_current_inject(Cell='PN_C', inj_amp=300,inj_dur=500,inj_delay=100)
#plot_current_inject(Cell='InterneuronCellf', inj_amp=300,inj_dur=500,inj_delay=100)
#plot_current_inject(Cell='SOM_Cell', inj_amp=300,inj_dur=500,inj_delay=100)

