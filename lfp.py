import h5py
import matplotlib.pyplot as plt
from scipy.signal import welch

f = h5py.File('outputECP_lowerthres2_lowlearn_5000_just_tone_baseline/ecp.h5','r')
data = f['ecp']['data'][50000:][::10].reshape(-1,)
freq, psd = plt.psd(data, NFFT=1024, Fs=1000)
plt.xlim(0,140)
plt.show()
