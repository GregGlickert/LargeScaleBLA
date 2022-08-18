import glob
import json
import os

from bmtk.simulator.bionet.pyfunction_cache import add_synapse_model
from neuron import h
import numpy as np
import random

def lognorm(mean,std):
    mean = float(mean)
    std = float(std)
    mean_ = np.log(mean) - 0.5 * np.log((std/mean)**2+1)
    std_ = np.sqrt(np.log((std/mean)**2 + 1))
    return float(np.random.lognormal(mean_,std_))

def Bg2Pyr(syn_params, sec_x, sec_id):
    """Create a bg2pyr synapse
    :param syn_params: parameters of a synapse
    :param sec_x: normalized distance along the section
    :param sec_id: target section
    :return: NEURON synapse object
    """

    lsyn = h.bg2pyr(sec_x, sec=sec_id)

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params['initW'])
    if syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])
    if syn_params.get('Percent_NMDA_block'): # from 0 to 1
        if float(syn_params['Percent_NMDA_block']) >= random.uniform(0,1):
            lsyn.gNMDAmax = float(0.5*10**-9)
        else:
            pass

    return lsyn

def bginh(syn_params, sec_x, sec_id):

    lsyn = h.bginh(sec_x, sec=sec_id)

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params['initW'])
    elif syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])
    
    if syn_params.get("AlphaTmax_gaba"):
        lsyn.AlphaTmax_gaba = float(syn_params['AlphaTmax_gaba'])
    if syn_params.get("Beta_gaba"):
        lsyn.Beta_gaba = float(syn_params['Beta_gaba'])

    return lsyn

def interD2interD_STFD(syn_params, sec_x, sec_id):

    lsyn = h.interD2interD_STFD(sec_x, sec=sec_id)

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params['initW'])
    elif syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])

    return lsyn

def interD2pyrD_STFD(syn_params, sec_x, sec_id):

    lsyn = h.interD2pyrD_STFD(sec_x, sec=sec_id)

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params['initW'])
    elif syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])
    if syn_params.get('threshold1'):
        lsyn.threshold1 = float(syn_params['threshold1'])  # par.x(8)
    if syn_params.get('threshold2'):
        lsyn.threshold2 = float(syn_params['threshold2'])  # par.x(9)

    return lsyn

def pyrD2interD_STFD(syn_params, sec_x, sec_id):
    
    lsyn = h.pyrD2interD_STFD(sec_x, sec=sec_id)

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params['initW'])
    if syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])
    if syn_params.get('threshold1'):
        lsyn.threshold1 = float(syn_params['threshold1'])  # par.x(8)
    if syn_params.get('threshold2'):
        lsyn.threshold2 = float(syn_params['threshold2'])  # par.x(9)
    if syn_params.get('Percent_NMDA_block'): # from 0 to 1
        if float(syn_params['Percent_NMDA_block']) >= random.uniform(0,1):
            lsyn.gbar_nmda = float(0.5*10**-9)
        else:
            pass


    return lsyn

def pyrD2pyrD_STFD(syn_params, sec_x, sec_id):
    
    lsyn = h.pyrD2pyrD_STFD(sec_x, sec=sec_id)

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params['initW'])
    elif syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])
    if syn_params.get('threshold1'):
        lsyn.threshold1 = float(syn_params['threshold1'])  # par.x(8)
    if syn_params.get('threshold2'):
        lsyn.threshold2 = float(syn_params['threshold2'])  # par.x(9)
    if syn_params.get('Percent_NMDA_block'): # from 0 to 1
        if float(syn_params['Percent_NMDA_block']) >= random.uniform(0,1):
            lsyn.gbar_nmda = float(0.5*10**-9)
        else:
            pass
        
    return lsyn

def pyrD2interD_P2SOM_STFD(syn_params, sec_x, sec_id):
    
    lsyn = h.pyrD2interD_P2SOM_STFD(sec_x, sec=sec_id)

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params['initW'])
    elif syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])
    if syn_params.get('Percent_NMDA_block'): # from 0 to 1
        if float(syn_params['Percent_NMDA_block']) >= random.uniform(0,1):
            lsyn.gbar_nmda = float(0.5*10**-9)
        else:
            pass

    return lsyn

def interD2pyrD_SOM2P_STFD(syn_params, sec_x, sec_id):

    lsyn = h.interD2pyrD_SOM2P_STFD(sec_x, sec=sec_id)

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params['initW'])
    elif syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])

    return lsyn

def pyrD2interD_P2CR_STFD(syn_params, sec_x, sec_id):

    lsyn = h.pyrD2interD_P2CR_STFD(sec_x, sec=sec_id)

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params['initW'])
    elif syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])

    return lsyn

def interD2pyrD_CR2P_STFD(syn_params, sec_x, sec_id):

    lsyn = h.interD2pyrD_CR2P_STFD(sec_x, sec=sec_id)

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params['initW'])
    elif syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])

    return lsyn

def interD2interD_SOMPV_STFD(syn_params, sec_x, sec_id):

    lsyn = h.interD2interD_SOMPV_STFD(sec_x, sec=sec_id)

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params['initW'])
    elif syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])

    return lsyn

def tone2pyrD(syn_params, sec_x, sec_id):
    """Create a tone2pyr synapse
    :param syn_params: parameters of a synapse
    :param sec_x: normalized distance along the section
    :param sec_id: target section
    :return: NEURON synapse object
    """
    lsyn = h.tone2pyr(sec_x, sec=sec_id)

    if syn_params.get('AlphaTmax_ampa'):
        lsyn.AlphaTmax_ampa = float(syn_params['AlphaTmax_ampa'])  # par.x(21)
    if syn_params.get('Beta_ampa'):
        lsyn.Beta_ampa = float(syn_params['Beta_ampa'])  # par.x(22)
    if syn_params.get('Cdur_ampa'):
        lsyn.Cdur_ampa = float(syn_params['Cdur_ampa'])  # par.x(23)
    if syn_params.get('gbar_ampa'):
        lsyn.gbar_ampa = float(syn_params['gbar_ampa'])  # par.x(24)
    if syn_params.get('Erev_ampa'):
        lsyn.Erev_ampa = float(syn_params['Erev_ampa'])  # par.x(16)

    if syn_params.get('AlphaTmax_nmda'):
        lsyn.AlphaTmax_nmda = float(syn_params['AlphaTmax_nmda'])  # par.x(25)
    if syn_params.get('Beta_nmda'):
        lsyn.Beta_nmda = float(syn_params['Beta_nmda'])  # par.x(26)
    if syn_params.get('Cdur_nmda'):
        lsyn.Cdur_nmda = float(syn_params['Cdur_nmda'])  # par.x(27)
    if syn_params.get('gbar_nmda'):
        lsyn.gbar_nmda = float(syn_params['gbar_nmda'])  # par.x(28)
    if syn_params.get('Erev_nmda'):
        lsyn.Erev_nmda = float(syn_params['Erev_nmda'])  # par.x(16)

    if syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])
    if syn_params.get('Percent_NMDA_block'): # from 0 to 1
        if float(syn_params['Percent_NMDA_block']) >= random.uniform(0,1):
            lsyn.gbar_nmda = float(0.5*10**-9)
        else:
            pass

    if syn_params.get('Wmax'):
        lsyn.Wmax = float(syn_params['Wmax']) * lsyn.initW  # par.x(1) * lsyn.initW
    if syn_params.get('Wmin'):
        lsyn.Wmin = float(syn_params['Wmin']) * lsyn.initW  # par.x(2) * lsyn.initW
    # delay = float(syn_params['initW']) # par.x(3) + delayDistance
    # lcon = new NetCon(&v(0.5), lsyn, 0, delay, 1)

    if syn_params.get('lambda1'):
        lsyn.lambda1 = float(syn_params['lambda1'])  # par.x(6)
    if syn_params.get('lambda2'):
        lsyn.lambda2 = float(syn_params['lambda2'])  # par.x(7)
    if syn_params.get('threshold1'):
        lsyn.threshold1 = float(syn_params['threshold1'])  # par.x(8)
    if syn_params.get('threshold2'):
        lsyn.threshold2 = float(syn_params['threshold2'])  # par.x(9)
    if syn_params.get('tauD1'):
        lsyn.tauD1 = float(syn_params['tauD1'])  # par.x(10)
    if syn_params.get('d1'):
        lsyn.d1 = float(syn_params['d1'])  # par.x(11)
    if syn_params.get('tauD2'):
        lsyn.tauD2 = float(syn_params['tauD2'])  # par.x(12)
    if syn_params.get('d2'):
        lsyn.d2 = float(syn_params['d2'])  # par.x(13)
    if syn_params.get('tauF'):
        lsyn.tauF = float(syn_params['tauF'])  # par.x(14)
    if syn_params.get('f'):
        lsyn.f = float(syn_params['f'])  # par.x(15)

    if syn_params.get('bACH'):
        lsyn.bACH = float(syn_params['bACH'])  # par.x(17)
    if syn_params.get('aDA'):
        lsyn.aDA = float(syn_params['aDA'])  # par.x(18)
    if syn_params.get('bDA'):
        lsyn.bDA = float(syn_params['bDA'])  # par.x(19)
    if syn_params.get('wACH'):
        lsyn.wACH = float(syn_params['wACH'])  # par.x(20)

    return lsyn

def tone2interD(syn_params, sec_x, sec_id):
    """Create a tone2pyr synapse
    :param syn_params: parameters of a synapse
    :param sec_x: normalized distance along the section
    :param sec_id: target section
    :return: NEURON synapse object
    """
    lsyn = h.tone2interD(sec_x, sec=sec_id)

    if syn_params.get('AlphaTmax_ampa'):
        lsyn.AlphaTmax_ampa = float(syn_params['AlphaTmax_ampa'])  # par.x(21)
    if syn_params.get('Beta_ampa'):
        lsyn.Beta_ampa = float(syn_params['Beta_ampa'])  # par.x(22)
    if syn_params.get('Cdur_ampa'):
        lsyn.Cdur_ampa = float(syn_params['Cdur_ampa'])  # par.x(23)
    if syn_params.get('gbar_ampa'):
        lsyn.gbar_ampa = float(syn_params['gbar_ampa'])  # par.x(24)
    if syn_params.get('Erev_ampa'):
        lsyn.Erev_ampa = float(syn_params['Erev_ampa'])  # par.x(16)

    if syn_params.get('AlphaTmax_nmda'):
        lsyn.AlphaTmax_nmda = float(syn_params['AlphaTmax_nmda'])  # par.x(25)
    if syn_params.get('Beta_nmda'):
        lsyn.Beta_nmda = float(syn_params['Beta_nmda'])  # par.x(26)
    if syn_params.get('Cdur_nmda'):
        lsyn.Cdur_nmda = float(syn_params['Cdur_nmda'])  # par.x(27)
    if syn_params.get('gbar_nmda'):
        lsyn.gbar_nmda = float(syn_params['gbar_nmda'])  # par.x(28)
    if syn_params.get('Erev_nmda'):
        lsyn.Erev_nmda = float(syn_params['Erev_nmda'])  # par.x(16)

    if syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])
    if syn_params.get('Percent_NMDA_block'): # from 0 to 1
        if float(syn_params['Percent_NMDA_block']) >= random.uniform(0,1):
            lsyn.gbar_nmda = float(0.5*10**-9)
        else:
            pass

    if syn_params.get('Wmax'):
        lsyn.Wmax = float(syn_params['Wmax']) * lsyn.initW  # par.x(1) * lsyn.initW
    if syn_params.get('Wmin'):
        lsyn.Wmin = float(syn_params['Wmin']) * lsyn.initW  # par.x(2) * lsyn.initW
    # delay = float(syn_params['initW']) # par.x(3) + delayDistance
    # lcon = new NetCon(&v(0.5), lsyn, 0, delay, 1)

    if syn_params.get('lambda1'):
        lsyn.lambda1 = float(syn_params['lambda1'])  # par.x(6)
    if syn_params.get('lambda2'):
        lsyn.lambda2 = float(syn_params['lambda2'])  # par.x(7)
    if syn_params.get('threshold1'):
        lsyn.threshold1 = float(syn_params['threshold1'])  # par.x(8)
    if syn_params.get('threshold2'):
        lsyn.threshold2 = float(syn_params['threshold2'])  # par.x(9)
    if syn_params.get('tauD1'):
        lsyn.tauD1 = float(syn_params['tauD1'])  # par.x(10)
    if syn_params.get('d1'):
        lsyn.d1 = float(syn_params['d1'])  # par.x(11)
    if syn_params.get('tauD2'):
        lsyn.tauD2 = float(syn_params['tauD2'])  # par.x(12)
    if syn_params.get('d2'):
        lsyn.d2 = float(syn_params['d2'])  # par.x(13)
    if syn_params.get('tauF'):
        lsyn.tauF = float(syn_params['tauF'])  # par.x(14)
    if syn_params.get('f'):
        lsyn.f = float(syn_params['f'])  # par.x(15)

    if syn_params.get('bACH'):
        lsyn.bACH = float(syn_params['bACH'])  # par.x(17)
    if syn_params.get('aDA'):
        lsyn.aDA = float(syn_params['aDA'])  # par.x(18)
    if syn_params.get('bDA'):
        lsyn.bDA = float(syn_params['bDA'])  # par.x(19)
    if syn_params.get('wACH'):
        lsyn.wACH = float(syn_params['wACH'])  # par.x(20)

    return lsyn

def Shock2Int(syn_params, sec_x, sec_id):
    """Create a int2pyr synapse
    :param syn_params: parameters of a synapse
    :param sec_x: normalized distance along the section
    :param sec_id: target section
    :return: NEURON synapse object
    """

    lsyn = h.shock2int(sec_x, sec=sec_id)

    if syn_params.get('AlphaTmax_ampa'):
        lsyn.AlphaTmax_ampa = float(syn_params['AlphaTmax_ampa'])  # par.x(21)
    if syn_params.get('Beta_ampa'):
        lsyn.Beta_ampa = float(syn_params['Beta_ampa'])  # par.x(22)
    if syn_params.get('Cdur_ampa'):
        lsyn.Cdur_ampa = float(syn_params['Cdur_ampa'])  # par.x(23)
    if syn_params.get('gbar_ampa'):
        lsyn.gbar_ampa = float(syn_params['gbar_ampa'])  # par.x(24)
    if syn_params.get('Erev_ampa'):
        lsyn.Erev_ampa = float(syn_params['Erev_ampa'])  # par.x(16)

    if syn_params.get('AlphaTmax_nmda'):
        lsyn.AlphaTmax_nmda = float(syn_params['AlphaTmax_nmda'])  # par.x(25)
    if syn_params.get('Beta_nmda'):
        lsyn.Beta_nmda = float(syn_params['Beta_nmda'])  # par.x(26)
    if syn_params.get('Cdur_nmda'):
        lsyn.Cdur_nmda = float(syn_params['Cdur_nmda'])  # par.x(27)
    if syn_params.get('gbar_nmda'):
        lsyn.gbar_nmda = float(syn_params['gbar_nmda'])  # par.x(28)
    if syn_params.get('Erev_nmda'):
        lsyn.Erev_nmda = float(syn_params['Erev_nmda'])  # par.x(16)

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params['initW'])  # * random.uniform(0.5,1.0) # par.x(0) * rC.uniform(0.5,1.0)//rand.normal(0.5,1.5) //`rand.repick()

    if syn_params.get('Wmax'):
        lsyn.Wmax = float(syn_params['Wmax']) * lsyn.initW  # par.x(1) * lsyn.initW
    if syn_params.get('Wmin'):
        lsyn.Wmin = float(syn_params['Wmin']) * lsyn.initW  # par.x(2) * lsyn.initW
    # delay = float(syn_params['initW']) # par.x(3) + delayDistance
    # lcon = new NetCon(&v(0.5), lsyn, 0, delay, 1)

    if syn_params.get('lambda1'):
        lsyn.lambda1 = float(syn_params['lambda1'])  # par.x(6)
    if syn_params.get('lambda2'):
        lsyn.lambda2 = float(syn_params['lambda2'])  # par.x(7)
    if syn_params.get('threshold1'):
        lsyn.threshold1 = float(syn_params['threshold1'])  # par.x(8)
    if syn_params.get('threshold2'):
        lsyn.threshold2 = float(syn_params['threshold2'])  # par.x(9)
    if syn_params.get('tauD1'):
        lsyn.tauD1 = float(syn_params['tauD1'])  # par.x(10)
    if syn_params.get('d1'):
        lsyn.d1 = float(syn_params['d1'])  # par.x(11)
    if syn_params.get('tauD2'):
        lsyn.tauD2 = float(syn_params['tauD2'])  # par.x(12)
    if syn_params.get('d2'):
        lsyn.d2 = float(syn_params['d2'])  # par.x(13)
    if syn_params.get('tauF'):
        lsyn.tauF = float(syn_params['tauF'])  # par.x(14)
    if syn_params.get('f'):
        lsyn.f = float(syn_params['f'])  # par.x(15)

    return lsyn


def load():
    add_synapse_model(Bg2Pyr, 'bg2pyr', overwrite=False)
    add_synapse_model(Bg2Pyr, overwrite=False)
    add_synapse_model(bginh, 'bginh', overwrite=False)
    add_synapse_model(bginh, overwrite=False)
    add_synapse_model(interD2interD_STFD, 'interD2interD_STFD', overwrite=False)
    add_synapse_model(interD2interD_STFD, overwrite=False)
    add_synapse_model(interD2pyrD_STFD, 'interD2pyrD_STFD', overwrite=False)
    add_synapse_model(interD2pyrD_STFD, overwrite=False)
    add_synapse_model(pyrD2interD_STFD, 'pyrD2interD_STFD', overwrite=False)
    add_synapse_model(pyrD2interD_STFD, overwrite=False)
    add_synapse_model(pyrD2pyrD_STFD, 'pyrD2pyrD_STFD', overwrite=False)
    add_synapse_model(pyrD2pyrD_STFD, overwrite=False)

    #SOM
    add_synapse_model(pyrD2interD_P2SOM_STFD, 'pyrD2interD_P2SOM_STFD', overwrite=False)
    add_synapse_model(pyrD2interD_P2SOM_STFD, overwrite=False)
    add_synapse_model(interD2pyrD_SOM2P_STFD, 'interD2pyrD_SOM2P_STFD', overwrite=False)
    add_synapse_model(interD2pyrD_SOM2P_STFD, overwrite=False)
    add_synapse_model(interD2interD_SOMPV_STFD, 'interD2interD_SOMPV_STFD', overwrite=False)
    add_synapse_model(interD2interD_SOMPV_STFD, overwrite=False)

    #CR
    add_synapse_model(pyrD2interD_P2CR_STFD, 'pyrD2interD_P2CR_STFD', overwrite=False)
    add_synapse_model(pyrD2interD_P2CR_STFD, overwrite=False)
    add_synapse_model(interD2pyrD_CR2P_STFD, 'interD2pyrD_CR2P_STFD', overwrite=False)
    add_synapse_model(interD2pyrD_CR2P_STFD, overwrite=False)

    #tone
    add_synapse_model(tone2pyrD, 'tone2pyrD', overwrite=False)
    add_synapse_model(tone2pyrD, overwrite=False)

    add_synapse_model(tone2interD, 'tone2interD', overwrite=False)
    add_synapse_model(tone2interD, overwrite=False)

    #shock
    add_synapse_model(Shock2Int, 'shock2int', overwrite=False)
    add_synapse_model(Shock2Int, overwrite=False)

    return

def syn_params_dicts(syn_dir='components/synaptic_models'):
    """
    returns: A dictionary of dictionaries containing all
    properties in the synapse json files
    """
    files = glob.glob(os.path.join(syn_dir,'*.json'))
    data = {}
    for fh in files:
        with open(fh) as f:
            data[os.path.basename(fh)] = json.load(f) #data["filename.json"] = {"prop1":"val1",...}
    return data
