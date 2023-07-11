import matplotlib.pyplot as plt
from fooof import FOOOF
from fooof.sim.gen import gen_aperiodic
from fooof.plts.spectra import plot_spectrum
from fooof.plts.annotate import plot_annotated_peak_search
from fooof.plts.annotate import plot_annotated_model
import h5py
import numpy as np
from scipy.signal import welch,decimate
from scipy.signal.windows import hann as hanning


ecp_h5_location = 'outputECP/ecp.h5'
f = h5py.File(ecp_h5_location)
data_raw = np.array(f['ecp']['data'])
ecp = data_raw.T[0] #flip verts and grab channel 0
ecp2 = np.loadtxt("LFP_elec_0")

nfft=1024
ecp = ecp[5000:]
win = hanning(nfft, True)
fs=500
lfp_d = decimate(ecp,20)
freqs,spectrum = welch(lfp_d,fs=fs,nfft=nfft)

#withoout

freqs_wo,spectrum_wo = welch(ecp,fs=1000,nfft=1024)
freqs_feng,spectrum_feng = welch(ecp2,fs=1000,nfft=1024)


plt_log = False
fm = FOOOF(aperiodic_mode='knee')
fm.fit(freqs_wo, spectrum_wo)
ap_fit = fm._ap_fit

init_flat_spec = spectrum_wo[1:] - 10**ap_fit

plt.plot(freqs_wo,spectrum_wo)

#plt.plot(residual_spec)
#plt.xlim((0,150))
plt.savefig("fooof.png")