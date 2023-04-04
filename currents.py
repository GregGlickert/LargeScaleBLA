import h5py
import pandas as pd
from bmtk.utils.reports.compartment import CompartmentReport
from tqdm import tqdm

def sum_current(path):
    print("Summing", path)
    report = CompartmentReport(path)
    array = report.data()
    current_array = []
    node_id = []
    for i in tqdm(range(800)):
        data = report.data(node_id=i)
        data = sum(sum(data))
        current_array.append(data)
        node_id.append(i)

    return current_array, node_id

def get_firing_rate(spike_path,node_id,total_seconds):
    f = h5py.File(spike_path)
    spikes_df = pd.DataFrame({'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})
    cell_spikes = spikes_df[spikes_df['node_ids'].isin(node_id)]
    spike_counts = cell_spikes.node_ids.value_counts()
    spike_counts_per_second = spike_counts / total_seconds
    return spike_counts_per_second


tone2PN_AMPA_current, nodes = sum_current('outputECP/tone2PN_i_AMPA.h5')
tone2PN_NMDA_current, nodes = sum_current('outputECP/tone2PN_i_NMDA.h5')

PN2PN_i_AMPA_current, nodes = sum_current('outputECP/AMPA_NMDA_STP_PN2PN_i_AMPA.h5')
PN2PN_i_NMDA_current, nodes = sum_current('outputECP/AMPA_NMDA_STP_PN2PN_i_NMDA.h5')

bg2pyr_AMPA_current, nodes = sum_current('outputECP/bg2pyr_i_AMPA.h5')
bg2pyr_NMDA_current, nodes = sum_current('outputECP/bg2pyr_i_NMDA.h5')

spikes = get_firing_rate('outputECP/spikes.h5')

all_data = list(zip(nodes,tone2PN_AMPA_current, tone2PN_NMDA_current,PN2PN_i_AMPA_current,PN2PN_i_NMDA_current,bg2pyr_AMPA_current,bg2pyr_NMDA_current))

df = pd.DataFrame(all_data,columns=['node_id','tone2PN_AMPA_current', 'tone2PN_NMDA_current',
                                    'PN2PN_i_AMPA_current','PN2PN_i_NMDA_current','bg2pyr_AMPA_current','bg2pyr_NMDA_current'])

df.to_csv("Currents.csv")