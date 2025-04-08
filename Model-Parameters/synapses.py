import glob
import json
import os

from bmtk.simulator.bionet.pyfunction_cache import add_synapse_model
from neuron import h
import numpy as np
import random

all_syn_block = True

rng = np.random.default_rng(0)

TEST_NUM = 20
TEST_COUNT1 = 0
TEST_COUNT2 = 0

LOGN_PARAM_DICT = {}

def get_logn_params(m, s, sigma_lower, sigma_upper):
    key = (m, s)
    params = LOGN_PARAM_DICT.get(key)
    if params is None:
        if m:
            sigma2 = np.log((s / m) ** 2 + 1)
            params = [np.log(m) - sigma2 / 2, sigma2 ** 0.5, {}]
        else:
            params = [-np.inf, 0., {}]
        LOGN_PARAM_DICT[key] = params
    key = (sigma_lower, sigma_upper)
    bounds = params[2].get(key)
    if bounds is None:
        mu, sigma = params[:2]
        lo = None if sigma_lower is None else np.exp(mu + sigma_lower * sigma)
        up = None if sigma_upper is None else np.exp(mu + sigma_upper * sigma)
        bounds = (lo, up)
        params[2][key] = bounds
    return params[0], params[1], bounds

def gen_logn_weight(mean, stdev, sigma_lower=None, sigma_upper=None):
    mu, sigma, bounds = get_logn_params(mean, stdev, sigma_lower, sigma_upper)
    weight = rng.lognormal(mu, sigma)
    if bounds[0] is not None:
        weight = max(weight, bounds[0])
    if bounds[1] is not None:
        weight = min(weight, bounds[1])
    return weight

def get_edge_prop_func(edge_props):
    """Get value from Edge object. Return None if property does not exist."""
    sonata_edge = edge_props._edge

    def get_edge_prop(key, default=None):
        return sonata_edge[key] if key in sonata_edge else default
    return get_edge_prop

def lognormal_weight(edge_props, source, target):
    """Function for synaptic weight between nodes"""
    get_edge_prop = get_edge_prop_func(edge_props)
    mean = get_edge_prop('syn_weight')
    if mean is None:
        weight = 1.0
    else:
        stdev = get_edge_prop('weight_sigma')
        if stdev:
            weight = gen_logn_weight(
                mean, stdev,
                sigma_lower=get_edge_prop('sigma_lower_bound'),
                sigma_upper=get_edge_prop('sigma_upper_bound'))
        else:
            weight = mean
        # global TEST_COUNT1
        # if TEST_COUNT1 < TEST_NUM:
        #     print(f'Synapse weight: {weight: .4g}')
        #     TEST_COUNT1 += 1
    return weight

def set_syn_weight(syn, syn_params):
    """Change initW property in synapse point process.
    Alternative method to change synaptic weight."""
    initW = syn_params.get('initW')
    stdevW = syn_params.get('stdevW')
    if initW is not None:
        if stdevW:
            initW = gen_logn_weight(
                initW, stdevW,
                sigma_lower=syn_params.get('sigma_lower_bound'),
                sigma_upper=syn_params.get('sigma_upper_bound'))
        syn.initW = initW
        # global TEST_COUNT2
        # if TEST_COUNT2 < TEST_NUM:
        #     print(f'Synapse initW: {initW: .4g}')
        #     TEST_COUNT2 += 1
        

def lognorm(mean,std):
    mean = float(mean)
    std = float(std)
    mean_ = np.log(mean) - 0.5 * np.log((std/mean)**2+1)
    std_ = np.sqrt(np.log((std/mean)**2 + 1))
    num = float(np.random.lognormal(mean_,std_))
    if num > mean*5:    #limit weights 
        num = mean*5
    return num

def Bg2Pyr(syn_params, sec_x, sec_id):
    """Create a bg2pyr synapse
    :param syn_params: parameters of a synapse
    :param sec_x: normalized distance along the section
    :param sec_id: target section
    :return: NEURON synapse object
    """

    lsyn = h.bg2pyr(sec_x, sec=sec_id)
    if syn_params.get('bACH'):
        if hasattr(lsyn, 'bACH'):
            lsyn.bACH = float(syn_params['bACH'])

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params['initW'])
    elif syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])

    if syn_params.get('Percent_NMDA_block'): # from 0 to 1
        if all_syn_block == False:
            if float(syn_params['Percent_NMDA_block']) >= random.uniform(0,1):
                lsyn.gNMDAmax = float(0.5*10**-9)
                pass
            else:
                pass
        if all_syn_block == True:
            lsyn.gNMDAmax = float((1-float(syn_params['Percent_NMDA_block'])) * 0.5e-3) #default NMDA_max
            pass


    return lsyn

def bginh(syn_params, sec_x, sec_id):

    lsyn = h.bginh(sec_x, sec=sec_id)
    if syn_params.get('bACH'):
        if hasattr(lsyn, 'bACH'):
            lsyn.bACH = float(syn_params['bACH'])

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
    if syn_params.get('bACH'):
        if hasattr(lsyn, 'bACH'):
            lsyn.bACH = float(syn_params['bACH'])

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params['initW'])
    elif syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])

    if syn_params.get('Beta_gaba'):
        lsyn.Beta_gaba = float(syn_params['Beta_gaba'])

    return lsyn

def interD2pyrD_STFD(syn_params, sec_x, sec_id):

    lsyn = h.interD2pyrD_STFD(sec_x, sec=sec_id)
    if syn_params.get('bACH'):
        if hasattr(lsyn, 'bACH'):
            lsyn.bACH = float(syn_params['bACH'])

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params['initW'])
    elif syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])

    if syn_params.get('Beta_gaba'):
        lsyn.Beta_gaba = float(syn_params['Beta_gaba'])


    return lsyn

def pyrD2interD_STFD(syn_params, sec_x, sec_id):
    if syn_params.get('use_bluebrain') == "False":
        lsyn = h.pyrD2interD_STFD(sec_x, sec=sec_id)
        if syn_params.get('bACH'):
            if hasattr(lsyn, 'bACH'):
                lsyn.bACH = float(syn_params['bACH'])

        if syn_params.get('initW'):
            lsyn.initW = float(syn_params['initW'])
        elif syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
            lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])

    if syn_params.get('use_bluebrain') == "True":
        lsyn = h.AMPA_NMDA_STP_LTP_PN2PV(sec_x, sec=sec_id)
        if syn_params.get('initW'):
            lsyn.initW = float(syn_params['initW'])
        elif syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
            lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])
            
        if syn_params.get('Percent_NMDA_block'): # from 0 to 1
            if all_syn_block == False:
                if float(syn_params['Percent_NMDA_block']) >= random.uniform(0,1):
                    lsyn.gmax_NMDA = float(0.55*10**-9)
                else:
                    pass
            if all_syn_block == True:
                lsyn.gmax_NMDA = float((1-float(syn_params['Percent_NMDA_block'])) * 0.55) #default NMDA_max

        lsyn.tau_r_AMPA = float(syn_params['tau_r_AMPA'])
        lsyn.tau_d_AMPA = float(syn_params['tau_d_AMPA'])
        lsyn.tau_r_NMDA = float(syn_params['tau_r_NMDA'])
        lsyn.tau_d_NMDA = float(syn_params['tau_d_NMDA'])
        if syn_params.get('theta_d_GB'):
            lsyn.theta_d_GB = float(syn_params['theta_d_GB'])
        if syn_params.get('theta_p_GB'):
            lsyn.theta_p_GB = float(syn_params['theta_p_GB'])

    return lsyn

def pyrD2pyrD_STFD(syn_params, sec_x, sec_id):
    if syn_params.get('use_bluebrain') == "False":
        lsyn = h.pyrD2pyrD_STFD(sec_x, sec=sec_id)
        if syn_params.get('bACH'):
            if hasattr(lsyn, 'bACH'):
                lsyn.bACH = float(syn_params['bACH'])

        if syn_params.get('initW'):
            lsyn.initW = float(syn_params['initW'])
        elif syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
            lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])
    
    if syn_params.get('use_bluebrain') == "True":
        lsyn = h.AMPA_NMDA_STP_PN2PN(sec_x, sec=sec_id)
        if syn_params.get('initW'):
            lsyn.initW = float(syn_params['initW'])

        if syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
            lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])

        if syn_params.get('Percent_NMDA_block'): # from 0 to 1
            if all_syn_block == False:
                if float(syn_params['Percent_NMDA_block']) >= random.uniform(0,1):
                    lsyn.gmax_NMDA = float(0.55*10**-9)
                else:
                    pass
            if all_syn_block == True:
                lsyn.gmax_NMDA = float((1-float(syn_params['Percent_NMDA_block'])) * 0.55) #default NMDA_max
    
    if syn_params.get('tau_r_AMPA'):
        lsyn.tau_r_AMPA = float(syn_params['tau_r_AMPA'])
    if syn_params.get('tau_d_AMPA'):
        lsyn.tau_r_AMPA = float(syn_params['tau_d_AMPA'])
    if syn_params.get('tau_d_AMPA'):
        lsyn.tau_r_AMPA = float(syn_params['Use'])
    if syn_params.get('tau_d_AMPA'):
        lsyn.tau_r_AMPA = float(syn_params['Dep'])
    if syn_params.get('tau_d_AMPA'):
        lsyn.tau_r_AMPA = float(syn_params['Fac'])
    return lsyn

def pyrD2interD_P2SOM_STFD(syn_params, sec_x, sec_id):
    if syn_params.get('use_bluebrain') == "False":
        lsyn = h.pyrD2interD_P2SOM_STFD(sec_x, sec=sec_id)
        if syn_params.get('bACH'):
            if hasattr(lsyn, 'bACH'):
                lsyn.bACH = float(syn_params['bACH'])

        if syn_params.get('initW'):
            lsyn.initW = float(syn_params['initW'])
        elif syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
            lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])

    if syn_params.get('use_bluebrain') == "True":
        lsyn = h.AMPA_NMDA_STP_PN2SOM(sec_x, sec=sec_id)
        if syn_params.get('initW'):
            lsyn.initW = float(syn_params['initW'])
        elif syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
            lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])

        if syn_params.get('Percent_NMDA_block'): # from 0 to 1
            if all_syn_block == False:
                if float(syn_params['Percent_NMDA_block']) >= random.uniform(0,1):
                    lsyn.gmax_NMDA = float(0.55*10**-9)
                else:
                    pass
            if all_syn_block == True:
                lsyn.gmax_NMDA = float((1-float(syn_params['Percent_NMDA_block'])) * 0.55) #default NMDA_max

    return lsyn

def interD2pyrD_SOM2P_STFD(syn_params, sec_x, sec_id):

    lsyn = h.interD2pyrD_SOM2P_STFD(sec_x, sec=sec_id)
    if syn_params.get('bACH'):
        if hasattr(lsyn, 'bACH'):
            lsyn.bACH = float(syn_params['bACH'])

    if syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])
        
    if syn_params.get('Beta_gaba'):
        lsyn.Beta_gaba = float(syn_params['Beta_gaba'])

    return lsyn

def pyrD2interD_P2CR_STFD(syn_params, sec_x, sec_id):

    lsyn = h.pyrD2interD_P2CR_STFD(sec_x, sec=sec_id)
    if syn_params.get('bACH'):
        if hasattr(lsyn, 'bACH'):
            lsyn.bACH = float(syn_params['bACH'])

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params['initW'])
    elif syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])

    return lsyn

def interD2pyrD_CR2P_STFD(syn_params, sec_x, sec_id):

    lsyn = h.interD2pyrD_CR2P_STFD(sec_x, sec=sec_id)
    if syn_params.get('bACH'):
        if hasattr(lsyn, 'bACH'):
            lsyn.bACH = float(syn_params['bACH'])

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params['initW'])
    elif syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])



    return lsyn

def interD2interD_SOMPV_STFD(syn_params, sec_x, sec_id):

    lsyn = h.interD2interD_SOMPV_STFD(sec_x, sec=sec_id)
    if syn_params.get('bACH'):
        if hasattr(lsyn, 'bACH'):
            lsyn.bACH = float(syn_params['bACH'])

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params['initW'])
    elif syn_params.get('initW_lognormal_mean') and syn_params.get('initW_lognormal_std'):
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean'],syn_params['initW_lognormal_std'])

    return lsyn

def tone2pyr(syn_params, sec_x, sec_id):
    """Create a tone2pyr synapse
    :param syn_params: parameters of a synapse
    :param sec_x: normalized distance along the section
    :param sec_id: target section
    :return: NEURON synapse object
    """
    if syn_params['use_blueBrain_synapse_with_LTP'] == 'True':
        lsyn = h.AMPA_NMDA_STP_LTP_tone2PN(sec_x, sec=sec_id)
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean_bb'],syn_params['initW_lognormal_std_bb'])
        lsyn.tau_r_AMPA = float(syn_params['tau_r_AMPA'])
        lsyn.tau_d_AMPA = float(syn_params['tau_d_AMPA'])
        lsyn.tau_r_NMDA = float(syn_params['tau_r_NMDA'])
        lsyn.tau_d_NMDA = float(syn_params['tau_d_NMDA'])

        lsyn.Fac_TM = float(syn_params['tau_f'])
        lsyn.Dep_TM = float(syn_params['tau_d'])
        lsyn.Use0_TM = float(syn_params['Use'])

        if syn_params.get('theta_d_GB'):
            lsyn.theta_d_GB = float(syn_params['theta_d_GB'])
        if syn_params.get('theta_p_GB'):
            lsyn.theta_p_GB = float(syn_params['theta_p_GB'])
        if syn_params.get('Percent_NMDA_block'): # from 0 to 1
            if all_syn_block == False:
                if float(syn_params['Percent_NMDA_block']) >= random.uniform(0,1):
                    lsyn.gmax_NMDA = float(0.55*10**-9)
                else:
                    pass
            if all_syn_block == True:
                lsyn.gmax_NMDA = float((1-float(syn_params['Percent_NMDA_block'])) * 0.55) #default NMDA_max

        if syn_params.get('Percent_AMPA_block'): # from 0 to 1
            if all_syn_block == False:
                if float(syn_params['Percent_AMPA_block']) >= random.uniform(0,1):
                    lsyn.gmax_AMPA  = float(0.55*10**-9)
                else:
                    pass
            if all_syn_block == True:
                lsyn.gmax_AMPA  = float((1-float(syn_params['Percent_AMPA_block'])) * 1) #default NMDA_max
            return lsyn

    if syn_params['use_blueBrain_synapse_with_LTP'] == 'False':
        lsyn = h.AMPA_NMDA_STP(sec_x, sec=sec_id)
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean_bb'],syn_params['initW_lognormal_std_bb'])
        lsyn.tau_r_AMPA = float(syn_params['tau_r_AMPA'])
        lsyn.tau_d_AMPA = float(syn_params['tau_d_AMPA'])
        lsyn.tau_r_NMDA = float(syn_params['tau_r_NMDA'])
        lsyn.tau_d_NMDA = float(syn_params['tau_d_NMDA'])
        if syn_params.get('Percent_NMDA_block'): # from 0 to 1
            if all_syn_block == False:
                if float(syn_params['Percent_NMDA_block']) >= random.uniform(0,1):
                    lsyn.gmax_NMDA = float(0.55*10**-9)
                else:
                    pass
            if all_syn_block == True:
                lsyn.gmax_NMDA = float((1-float(syn_params['Percent_NMDA_block'])) * 0.001) #default NMDA_max

        if syn_params.get('Percent_AMPA_block'): # from 0 to 1
            if all_syn_block == False:
                if float(syn_params['Percent_AMPA_block']) >= random.uniform(0,1):
                    lsyn.gmax_AMPA  = float(0.55*10**-9)
                else:
                    pass
            if all_syn_block == True:
                lsyn.gmax_AMPA  = float((1-float(syn_params['Percent_AMPA_block'])) * 0.001) #default NMDA_max
            return lsyn

def tone2pv(syn_params, sec_x, sec_id):
    """Create a tone2pyr synapse
    :param syn_params: parameters of a synapse
    :param sec_x: normalized distance along the section
    :param sec_id: target section
    :return: NEURON synapse object
    """
    if syn_params['use_blueBrain_synapse_with_LTP'] == 'True':
        lsyn = h.AMPA_NMDA_STP_LTP_tone2PV(sec_x, sec=sec_id)
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean_bb'],syn_params['initW_lognormal_std_bb'])
        lsyn.tau_r_AMPA = float(syn_params['tau_r_AMPA'])
        lsyn.tau_d_AMPA = float(syn_params['tau_d_AMPA'])
        lsyn.tau_r_NMDA = float(syn_params['tau_r_NMDA'])
        lsyn.tau_d_NMDA = float(syn_params['tau_d_NMDA'])

        lsyn.Fac_TM = float(syn_params['tau_f'])
        lsyn.Dep_TM = float(syn_params['tau_d'])
        lsyn.Use0_TM = float(syn_params['Use'])

        if syn_params.get('theta_d_GB'):
            lsyn.theta_d_GB = float(syn_params['theta_d_GB'])
        if syn_params.get('theta_p_GB'):
            lsyn.theta_p_GB = float(syn_params['theta_p_GB'])
        if syn_params.get('Percent_NMDA_block'): # from 0 to 1
            if all_syn_block == False:
                if float(syn_params['Percent_NMDA_block']) >= random.uniform(0,1):
                    lsyn.gmax_NMDA = float(0.55*10**-9)
                else:
                    pass
            if all_syn_block == True:
                lsyn.gmax_NMDA = float((1-float(syn_params['Percent_NMDA_block'])) * 0.55) #default NMDA_max

        if syn_params.get('Percent_AMPA_block'): # from 0 to 1
            if all_syn_block == False:
                if float(syn_params['Percent_AMPA_block']) >= random.uniform(0,1):
                    lsyn.gmax_AMPA  = float(0.55*10**-9)
                else:
                    pass
            if all_syn_block == True:
                lsyn.gmax_AMPA  = float((1-float(syn_params['Percent_AMPA_block'])) * 1) #default NMDA_max
            return lsyn

    if syn_params['use_blueBrain_synapse_with_LTP'] == 'False':
        lsyn = h.AMPA_NMDA_STP(sec_x, sec=sec_id)
        lsyn.initW = lognorm(syn_params['initW_lognormal_mean_bb'],syn_params['initW_lognormal_std_bb'])
        lsyn.tau_r_AMPA = float(syn_params['tau_r_AMPA'])
        lsyn.tau_d_AMPA = float(syn_params['tau_d_AMPA'])
        lsyn.tau_r_NMDA = float(syn_params['tau_r_NMDA'])
        lsyn.tau_d_NMDA = float(syn_params['tau_d_NMDA'])
        if syn_params.get('Percent_NMDA_block'): # from 0 to 1
            if all_syn_block == False:
                if float(syn_params['Percent_NMDA_block']) >= random.uniform(0,1):
                    lsyn.gmax_NMDA = float(0.55*10**-9)
                else:
                    pass
            if all_syn_block == True:
                lsyn.gmax_NMDA = float((1-float(syn_params['Percent_NMDA_block'])) * 0.001) #default NMDA_max

        if syn_params.get('Percent_AMPA_block'): # from 0 to 1
            if all_syn_block == False:
                if float(syn_params['Percent_AMPA_block']) >= random.uniform(0,1):
                    lsyn.gmax_AMPA  = float(0.55*10**-9)
                else:
                    pass
            if all_syn_block == True:
                lsyn.gmax_AMPA  = float((1-float(syn_params['Percent_AMPA_block'])) * 0.001) #default NMDA_max
            return lsyn

def shock2int(syn_params, sec_x, sec_id):
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

AMPA_NMDA_STP_params = ('tau_r_AMPA', 'tau_d_AMPA', 'Use', 'Dep', 'Fac')

def AMPA_NMDA_STP(syn_params, sec_x, sec_id):
    """Create a AMPA_NMDA_STP synapse
    :param syn_params: parameters of a synapse
    :param sec_x: normalized distance along the section
    :param sec_id: target section
    :return: NEURON synapse object
    """
    syn = h.AMPA_NMDA_STP(sec_x, sec=sec_id)
    for key in AMPA_NMDA_STP_params:
        value = syn_params.get(key)
        if value is not None:
            setattr(syn, key, value)
    set_syn_weight(syn, syn_params)
    return syn

def ampa_nmda_stp(syn_params, xs, secs):
    """Create a list of AMPA_NMDA_STP synapses
    :param syn_params: parameters of a synapse
    :param xs: list of normalized distances along the section
    :param secs: target sections
    :return: list of NEURON synpase objects
    """
    return [AMPA_NMDA_STP(syn_params, x, sec) for x, sec in zip(xs, secs)]

def load(randseed=1111, rng_obj=None):
    global rng
    if rng_obj is None:
        rng = np.random.default_rng(randseed)
    else:
        rng = rng_obj
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
    add_synapse_model(AMPA_NMDA_STP, 'AMPA_NMDA_STP', overwrite=False)

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

    #Tone
    add_synapse_model(tone2pyr, 'tone2pyr', overwrite=False)
    add_synapse_model(tone2pyr, overwrite=False)
    add_synapse_model(tone2pv, 'tone2pv', overwrite=False)
    add_synapse_model(tone2pv, overwrite=False)

    #Shock
    add_synapse_model(shock2int, 'shock2int', overwrite=False)
    add_synapse_model(shock2int, overwrite=False)

    return

def syn_params_dicts(syn_dir='components/synaptic_models'):
    """
    returns: A dictionary of dictionaries containing all
    properties in the synapse json files
    """
    files = glob.glob(os.path.join(syn_dir, '*.json'))
    data = {}
    for fh in files:
        with open(fh) as f:
            # data["filename.json"] = {"prop1":"val1", ...}
            data[os.path.basename(fh)] = json.load(f)
    return data
