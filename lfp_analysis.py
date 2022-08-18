from scipy.signal import hanning,welch,decimate, periodogram
import h5py
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

def raw_ecp(lfp):
    pass

def ecp_psd(ecp, skip_n=0, downsample=10, nfft=1024, fs=1000, noverlap=0, ax=None, temp = False):
    # skip_n first few
    data = ecp[skip_n:]

    # downsample the data to fit ms (steps used 20=1/.05 step)
    lfp_d = decimate(data, downsample)
    raw_ecp(lfp_d)
    win = hanning(nfft, True)

    f, pxx = welch(lfp_d, fs, window=win, noverlap=noverlap, nfft=nfft)

    ax.set_xscale('log')
    ax.set_yscale('log')
    if temp == False:
        ax.plot(f, pxx * 1000, linewidth=0.6)
    if temp == True:
        y = 1/f
        difference = (pxx*1000) - y
        ax.plot(f,y)
        ax.plot(f, pxx * 1000, linewidth=0.6)
        #ax.plot(f,difference)
        #ax.set_xlim(0.0001,500)
    ax.set_ylim([0.0000001, 100])

    theta = pxx[np.where((f > 8) & (f < 12))] * 1000
    gamma = pxx[np.where((f > 50) & (f < 80))] * 1000
    mean_theta = theta.mean()
    peak_theta = theta.max()
    mean_gamma = gamma.mean()
    peak_gamma = gamma.max()
    print('')
    print("Mean theta (8Hz-12Hz)  : " + str(mean_theta))
    print("Mean gamma (50Hz-60Hz) : " + str(mean_gamma))
    print('')
    print("Peak theta (8Hz-12Hz)  : " + str(peak_theta))
    print("Peak gamma (50Hz-60Hz) : " + str(peak_gamma))
    print('')

dt = 0.1
steps_per_ms = 1 / dt
skip_seconds = 5
skip_ms = skip_seconds * 1000
skip_n = int(skip_ms * steps_per_ms)
end_ms = 15000

spikes_location = 'baseline/spikes.h5'

print("loading " + spikes_location)
f = h5py.File(spikes_location)
spikes_df = pd.DataFrame(
    {'node_ids': f['spikes']['BLA']['node_ids'], 'timestamps': f['spikes']['BLA']['timestamps']})
print("done")

ecp_h5_location = 'baseline/ecp.h5'
print("loading " + ecp_h5_location)
ecp_channel = 0
f = h5py.File(ecp_h5_location)
data_raw = np.array(f['ecp']['data'])
ecp = data_raw.T[ecp_channel]  # flip verts and grab channel 0
print("done")

fig, ax = plt.subplots(1,1)

ecp_psd(ecp, skip_n=skip_n, ax=ax)
plt.show()
