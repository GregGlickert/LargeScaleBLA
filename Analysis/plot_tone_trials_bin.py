import h5py
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from scipy.stats import ttest_rel # for paired t-test
from scipy.stats import ttest_ind
import seaborn as sns
#plt.rcParams.update({'font.size': 16})

warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

scale = 1
node_set_split = [
    #{"name": "PN_A", "start": 0 * scale, "end": 568 * scale , "color": "blue"},
    #{"name": "PN_C", "start": 569 * scale, "end": 799 * scale, "color": "olive"},
    {"name": "PN", "start": 600 * scale, "end": 799 * scale, "color": "olive"},
    {"name": "PV", "start": 800 * scale, "end": 899 * scale, "color": "purple"},
    {"name": "SOM", "start": 899 * scale, "end": 999 * scale, "color": "green"}
    #{"name": "VIP", "start": 1000 * scale, "end": 1106 * scale + 3, "color": "brown"}
]

def tone_firing_rate(cell_ids,spike_path,tone_start,tone_trials_count):
    fig, ax = plt.subplots(1,1, figsize=(12, 6),tight_layout=True)
    f = h5py.File(spike_path)
    spikes_df = pd.DataFrame(
        {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})
    start = tone_start
    end = tone_start + 500
    spikes = []
    for i in range(tone_trials_count):
        cell_spikes = spikes_df
        print(start,end)
        # skip the first few ms
        cell_spikes = cell_spikes[cell_spikes['timestamps'] > start]
        cell_spikes = cell_spikes[cell_spikes['timestamps'] < end]
        spike_counts = cell_spikes.node_ids.value_counts()
        spike_counts_per_second = spike_counts/0.5
        spikes.append(spike_counts_per_second)
        spikes_mean = spike_counts_per_second.mean()
        spikes_std = spike_counts_per_second.std()

        print("trial{} mean {:.2f} std {:.2f}".format(i,spikes_mean,spikes_std))

        start = start + 1500
        end = end + 1500

    return spikes

def plot(node_set=None, tone_start=None, spikes_df=None, ax=None,tone_trial_count = 8, title=0):
    for node in node_set:
        if node['name'] == 'PN':
            cells = [2, 3, 4, 6, 7, 12, 13, 17, 20, 21, 22, 23, 24, 25, 26, 27, 29, 31, 36, 37, 38, 39, 42, 44, 46, 47, 48, 51, 52, 53, 54, 56, 57, 58, 60, 64, 65, 68, 69, 71, 72, 73, 76, 77, 80, 84, 87, 88, 89, 90, 91, 92, 98, 99, 101, 102, 103, 104, 107, 109, 110, 112, 115, 117, 119, 121, 126, 128, 129, 135, 136, 137, 140, 141, 142, 149, 153, 154, 156, 157, 161, 162, 165, 166, 167, 170, 173, 178, 180, 182, 184, 187, 188, 190, 191, 195, 196, 198, 199, 207, 212, 213, 215, 216, 218, 219, 222, 223, 225, 227, 231, 232, 235, 237, 238, 245, 247, 249, 254, 258, 264, 267, 268, 271, 273, 277, 279, 281, 283, 284, 288, 290, 291, 292, 295, 296, 300, 304, 305, 306, 308, 309, 312, 314, 315, 319, 321, 323, 325, 326, 329, 331, 332, 333, 334, 341, 344, 345, 347, 350, 351, 354, 356, 358, 364, 365, 366, 369, 371, 374, 376, 377, 379, 384, 385, 386, 389, 390, 391, 394, 395, 397, 399, 402, 403, 407, 409, 410, 411, 412, 414, 416, 417, 418, 421, 422, 423, 426, 427, 428, 430, 431, 433, 434, 436, 437, 444, 447, 449, 450, 453, 456, 458, 459, 461, 463, 465, 467, 470, 476, 478, 480, 485, 486, 487, 488, 489, 494, 497, 499, 502, 505, 507, 508, 509, 511, 512, 514, 521, 522, 523, 525, 528, 530, 533, 535, 538, 539, 541, 542, 546, 547, 549, 550, 551, 552, 558, 562, 563, 565, 567, 569, 570, 572, 573, 574, 575, 576, 577, 582, 583, 585, 586, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 610, 611, 613, 615, 616, 617, 620, 621, 622, 623, 625, 626, 627, 628, 629, 631, 633, 634, 637, 638, 640, 641, 642, 643, 645, 646, 648, 649, 651, 653, 654, 656, 657, 658, 659, 660, 661, 665, 667, 668, 670, 671, 672, 673, 674, 676, 677, 678, 679, 680, 681, 682, 684, 686, 688, 689, 690, 691, 692, 695, 696, 697, 698, 700, 704, 705, 706, 707, 708, 709, 710, 711, 712, 716, 718, 720, 722, 723, 725, 726, 728, 729, 730, 731, 732, 734, 735, 736, 738, 739, 741, 742, 743, 744, 746, 747, 749, 750, 751, 753, 756, 757, 758, 759, 760, 761, 764, 765, 767, 768, 770, 773, 776, 778, 780, 781, 782, 784, 785, 786, 787, 788, 789, 790, 791, 792, 794, 795, 796, 797, 798, 799]
            cells = range(node['start'], node['end'] + 1)  # +1 to be inclusive of last cell
        else:
            cells = range(node['start'], node['end'] + 1)  # +1 to be inclusive of last cell
        #if node['name'] != 'PN_C':
        #    break
        start = tone_start
        cell_spikes = spikes_df[spikes_df['node_ids'].isin(cells)]
        all_trials = pd.DataFrame(columns=['node_ids', 'timestamps'])
        end = start + 500
        for i in range(tone_trial_count):
            print(start, end)
            cell_spikes_temp = cell_spikes[cell_spikes['timestamps'] > start]
            cell_spikes_temp = cell_spikes_temp[cell_spikes['timestamps'] < end]
            all_trials = all_trials.append(cell_spikes_temp)
            start = start + 1500
            end = end + 1500

        spike_counts = all_trials.node_ids.value_counts()
        total_seconds = (tone_trial_count*500)/1000
        spike_counts = spike_counts / total_seconds

        spike_counts_mean = spike_counts.mean()
        spike_std = spike_counts.std()
        #ax.hist(spike_counts)
        #ax.bar(node['name'], spike_counts_mean, yerr=spike_std, align='center',color=node['color'],capsize=10,
        #       label='{} : {:.2f} ({:.2f})'.format(node['name'], spike_counts_mean, spike_std))

        sns.distplot(ax=ax,x=spike_counts, hist=False,label='{} : {:.2f} ({:.2f})'.format(node['name'], spike_counts_mean, spike_std))
        #if ax == axs[0]:
        #    ax.set_ylabel("mean Hz during tone")
        ax.set_title(title)
        #ax.set_ylim(0,60)
        ax.legend(loc=2, prop={'size': 8})
        return spike_counts


PN_array = range(800)
PV_array = range(800,900)
SOM_array = range(900,1000)

spike_path = 'outputECP_tone+shock/spikes.h5'
f = h5py.File(spike_path)
spikes_df = pd.DataFrame(
    {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})


tone_start = 5000 # time the tones start
tone_trials_count = 3 # 15000 = 8 number of trials during the sim

fig, axs = plt.subplots(1,2, figsize=(10, 6),tight_layout=True,sharey=True)
#plot(node_set=node_set_split,tone_start=tone_start, spikes_df=spikes_df, ax=axs, tone_trial_count= tone_trials_count, title="baseline NMDA conductance")
#spikes = tone_firing_rate(PN_array,spike_path,tone_start,tone_trials_count)
#plt.hist(spikes)
#plt.show()
# for tone trials its 5000 and 20000
first = plot(node_set=node_set_split,tone_start=5000, spikes_df=spikes_df, ax=axs[0], tone_trial_count= 5, title="First 5 tone trials")
last = plot(node_set=node_set_split,tone_start=36500, spikes_df=spikes_df, ax=axs[1], tone_trial_count= 5, title="Last 5 tone trials")
#plot(node_set=node_set_split,tone_start=3000, spikes_df=spikes_df2, ax=axs[2], tone_trial_count= 5, title="100% block")

t_value, p_value = ttest_ind(first,last)
print(p_value)
plt.savefig("tone+shock.png")
#plot(node_set=node_set_split,tone_start=30000, spikes_df=spikes_df, ax=axs, tone_trial_count= 5, title="baseline NMDA conductance")
#plt.show()