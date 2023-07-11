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


def cell_by_cell_z_score():
    f = h5py.File('outputECP_lowerthres2_lowlearn_5000/spikes.h5')

    def get_tone_firing(start,end,f):
        spikes_df = pd.DataFrame({'node_ids': f['spikes']['BLA']['node_ids'], 
                                'timestamps': f['spikes']['BLA']['timestamps']})
        spikes_df = spikes_df[spikes_df['timestamps'] > start]
        spikes_df = spikes_df[spikes_df['timestamps'] < end]
        spikes_df = spikes_df[spikes_df['node_ids']< 4000] #PN Cells
        #spike_counts = spikes_df.node_ids.value_counts(sort=False)
        #firing_rate = (spike_counts/0.5)
        return spikes_df
    
    pre_trial1 = get_tone_firing(start=5000,end=5500,f=f)
    pre_trial2 = get_tone_firing(start=6500,end=7000,f=f)
    pre_trial3 = get_tone_firing(start=8000,end=8500,f=f)
    pre_trial4 = get_tone_firing(start=9500,end=10000,f=f)
    pre_trial5 = get_tone_firing(start=11000,end=11500,f=f)
    post_trial1 = get_tone_firing(start=27500,end=28000,f=f)
    post_trial2 = get_tone_firing(start=29000,end=29500,f=f)
    post_trial3 = get_tone_firing(start=30500,end=31000,f=f)
    post_trial4 = get_tone_firing(start=32000,end=32500,f=f)
    post_trial5 = get_tone_firing(start=33500,end=34000,f=f)

    

cell_by_cell_z_score()