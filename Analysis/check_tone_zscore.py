import h5py
import pandas as pd
from scipy.stats import ttest_rel # for paired t-test
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
from statsmodels.stats.weightstats import ztest as ztest
from bmtk.utils.reports.compartment import CompartmentReport
from tqdm import tqdm


def population_z_score():
    f = h5py.File('outputECP_lowerthres2_lowlearn_5000/spikes.h5')
    before_tone_avg = pd.DataFrame(columns =['node_ids','timestamps'])
    start = 5000 
    end = 5500 
    for i in range(5):
        spikes_df = pd.DataFrame({'node_ids': f['spikes']['BLA']['node_ids'], 
                                'timestamps': f['spikes']['BLA']['timestamps']})
        #print(start,end)
        spikes_df = spikes_df[spikes_df['timestamps'] > start]
        spikes_df = spikes_df[spikes_df['timestamps'] < end]
        spikes_df = spikes_df[spikes_df['node_ids']< 4000] #PN Cells
        before_tone_avg = pd.concat([before_tone_avg,spikes_df])
        start = start + 1500
        end = end + 1500

    tone_response_avg = pd.DataFrame(columns =['node_ids','timestamps'])
    start = 27500 
    end = 28000 
    for i in range(5):
        spikes_df = pd.DataFrame({'node_ids': f['spikes']['BLA']['node_ids'], 
                                'timestamps': f['spikes']['BLA']['timestamps']})
    #print(start,end)
        spikes_df = spikes_df[spikes_df['timestamps'] > start]
        spikes_df = spikes_df[spikes_df['timestamps'] < end]
        spikes_df = spikes_df[spikes_df['node_ids'] < 4000] #PN Cells
        tone_response_avg = pd.concat([tone_response_avg,spikes_df])
        start = start + 1500
        end = end + 1500

    def spikes_per_second(dataframe, total_seconds):
        spike_counts = dataframe.node_ids.value_counts()
        spike_counts_per_second = spike_counts / total_seconds
        return spike_counts_per_second

    before_tone_avg = spikes_per_second(before_tone_avg,2.5)
    tone_response_avg = spikes_per_second(tone_response_avg,2.5)

    plt.hist(before_tone_avg)
    plt.figure(2)
    plt.hist(tone_response_avg)
    plt.show()

    t_stat, p_value = ttest_ind(before_tone_avg, tone_response_avg)
    print("T-statistic value: ", t_stat)  
    print("P-Value: ", p_value)

    z_score, p_value = ztest(before_tone_avg, tone_response_avg,value=0)
    print('z-score is', z_score)
    print('p-value from zscore is', p_value)


def cell_by_cell_z_score(pot_path=None):

    def get_firing_rate(df,start,end):
        spikes_df = df
        spikes_df = spikes_df[spikes_df['timestamps'] > start]
        spikes_df = spikes_df[spikes_df['timestamps'] < end]
        spike_counts = spikes_df.node_ids.value_counts()
        Hz = spike_counts/(0.3)
        return Hz.to_list()

    winners = []
    for g in tqdm(range(800)):
        f = h5py.File('outputECP_tone+shock_Wlimit3/spikes.h5')
        spikes_df = pd.DataFrame({'node_ids': f['spikes']['BLA']['node_ids'],
                                  'timestamps': f['spikes']['BLA']['timestamps']})
        
        spikes_df = spikes_df[spikes_df['node_ids'] == g] #change back to g

        hib_firing_rate_list = []
        tone_trials = 10
        hib_start = 5000
        for i in range(tone_trials):
            temp_hz = get_firing_rate(spikes_df,start=hib_start,end=hib_start+300)
            hib_start = hib_start + 1500
            if len(temp_hz)>0:
                 hib_firing_rate_list.extend(temp_hz)
            if len(temp_hz) == 0:
                 hib_firing_rate_list.append(0)

        cond_firing_rate_list = []
        tone_shock_trials = 16
        blocks = 4
        conditioning_start = 20000
        for i in range(1,17):
            temp_hz = get_firing_rate(spikes_df,start=conditioning_start,end=conditioning_start+300)
            conditioning_start = conditioning_start + 1500
            if len(temp_hz)>0:
                 cond_firing_rate_list.extend(temp_hz)
            if len(temp_hz) == 0:
                 cond_firing_rate_list.append(0)
            if i % 4 == 0:
                #print(i)
                #print(cond_firing_rate_list)
                z_score, p_value = ttest_ind(hib_firing_rate_list, cond_firing_rate_list)
                #print('z-score is', z_score)
                #print('p-value from zscore is', p_value)
                cond_firing_rate_list = [] #reset for next block
                if p_value < 0.0001: # can change to have less winners and 
                    report_pot = CompartmentReport(pot_path) 
                    data_pot = report_pot.data(node_id=g)
                    if 1 in data_pot: #check to make sure did an LTP at some point
                        winners.append(g)

    winners = sorted([*set(winners)]) #remove dups
    print(len(winners))
    print(winners)

    
    

cell_by_cell_z_score(pot_path='outputECP_tone+shock_Wlimit3/tone2PN_pot_flag.h5')