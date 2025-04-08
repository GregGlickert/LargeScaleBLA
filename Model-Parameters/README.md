# 1000 Large Scale model of the BLA 
## There are several different simulations the can be ran for this model. Each simulation config contains different simulation parameters. To change which simulation config is used you can run a different batch script.You can also change when the tone and shock are present by changing things in the build_inputs.py script.Finally you can change how long each simulation is ran for by changing tstop in each config.
| batch file |config      | run |
|----------- | ----------- | ----------- |
| batch_run_baseline | simulation_configECP_base_homogenous.json      | Baseline |
| batch_run_tone_trials.sh |simulation_configECP_trials_homogenous.json   | tone trials        |
| batch_run_tone_shock.sh |simulation_configECP_tone+shock_homogenous.json   | tone+shock conditioning        |
|  |


## To build the network
```
python build_network.py homogenous
```


## To build inputs
```
python build_input.py
```

## Compile mod files
```
cd components/mechanisms/
rm -rf x86_64/
nrnivmodl modfiles
cd ../..
```

## To run the model (replace batch_file with desired config)
```
sbatch batch_file.sh
```

## The next few scrips are used to look at how the network is build and to check connections present in the model
## To generate a csv called connection table containing import connectivity data
```
python connection_table.py
```

## To plot the convergence of the network
```
python plot_connections.py
```

## To print out precent connectivity NOT DISTANCE DEPENDENT
```
python connection_precent.py
```


## The next scripts are used to plot what is going on in the network. Each simulation config has a different name for the output folder it generates. When using the scripts make sure to change the output folder to be the simulation you want to plot. Some of the scripts may also have time windows to calculate different things. Make sure this window is correct to make sure that you use the script correctly.


## To plot a raster 
```
python plot_raster.py
```

## To plot a firing rate histogram
```
python plot_firing_rate_distro.py
```

## To view the FOOOF LFP
```
python Fooof_lfp.py
```

## To analysis tone reponse using zscore
```
python check_tone_zscore.py
```

## To check LTD/LTP rates for a cell 
```
python plot_syn_weight.py
```

## To plot the firing during tone trials
```
python plot_tone_trials_bin.py
```

