import h5py
import pandas as pd
from bmtk.utils.reports.compartment import CompartmentReport
from bmtk.analyzer.compartment import plot_traces
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

def sum_current(path):
    print("Summing", path)
    report = CompartmentReport(path)
    array = report.data()
    current_array = []
    node_id = []
    cells = report.node_ids()
    for i in tqdm(range(len(report.node_ids()))):
        if cells[i]>3050:
            pass
        else:
            data = report.data(node_id=cells[i])
            data = sum(sum(data))
            current_array.append(data)
            node_id.append(cells[i])

    return current_array, node_id

def get_firing_rate(spike_path,node_id,total_seconds):
    f = h5py.File(spike_path)
    spikes_df = pd.DataFrame({'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})
    cell_spikes = spikes_df[spikes_df['node_ids'].isin(node_id)]
    print(node_id)
    spike_counts = cell_spikes.node_ids.value_counts()
    spike_counts_per_second = spike_counts / total_seconds
    return spike_counts_per_second

#plot_traces(report_path="output_baseline/AMPA_NMDA_STP_PN2PN_i_NMDA.h5")

def process_currents():
    tone2PN_AMPA_current, nodes = sum_current('output_currents_baseline_blocked_server/tone2PN_i_AMPA.h5')
    tone2PN_NMDA_current, nodes = sum_current('output_currents_baseline_blocked_server/tone2PN_i_NMDA.h5')

    PN2PN_i_AMPA_current, nodes = sum_current('output_currents_baseline_blocked_server/AMPA_NMDA_STP_PN2PN_i_AMPA.h5')
    PN2PN_i_NMDA_current, nodes = sum_current('output_currents_baseline_blocked_server/AMPA_NMDA_STP_PN2PN_i_NMDA.h5')

    bg2pyr_AMPA_current, nodes = sum_current('output_currents_baseline_blocked_server/bg2pyr_i_AMPA.h5')
    bg2pyr_NMDA_current, nodes = sum_current('output_currents_baseline_blocked_server/bg2pyr_i_NMDA.h5')

    spikes = get_firing_rate('output_currents_baseline_blocked_server/spikes.h5',node_id=nodes,total_seconds=15)

    all_data = list(zip(nodes,tone2PN_AMPA_current, tone2PN_NMDA_current,PN2PN_i_AMPA_current,PN2PN_i_NMDA_current,bg2pyr_AMPA_current,bg2pyr_NMDA_current,spikes))

    df = pd.DataFrame(all_data,columns=['node_id','tone2PN_AMPA_current', 'tone2PN_NMDA_current',
                                        'PN2PN_i_AMPA_current','PN2PN_i_NMDA_current','bg2pyr_AMPA_current','bg2pyr_NMDA_current','spikes'])

    df.to_csv("Currents_blocked.csv")

def read_in(path):
    df = pd.read_csv(path)
    return df

def current_plot(current, label,ax):
    ax.hist(current)
    ax.set_ylabel("cells")
    ax.set_xlabel("Current")
    ax.set_title(label)

process_currents()

df = read_in("Currents_blocked.csv")

fig, axs = plt.subplots(3,2, figsize=(12, 6),tight_layout=True,sharey=True,sharex=True)

current_plot(df['tone2PN_AMPA_current'],label = 'tone2PN_AMPA_current',ax=axs[0,0])
current_plot(df['tone2PN_NMDA_current'],label = 'tone2PN_NMDA_current',ax=axs[0,1])
current_plot(df['PN2PN_i_AMPA_current'],label = 'PN2PN_i_AMPA_current',ax=axs[1,0])
current_plot(df['PN2PN_i_NMDA_current'],label = 'PN2PN_i_NMDA_current',ax=axs[1,1])
current_plot(df['bg2pyr_AMPA_current'],label = 'bg2pyr_AMPA_current',ax=axs[2,0])
current_plot(df['bg2pyr_NMDA_current'],label = 'bg2pyr_NMDA_current',ax=axs[2,1])

plt.suptitle("blocked baseline")
plt.show()