# Large Scale model of the BLA 
## There are several different simulations the can be ran for this model. Each simulation config contains different simulation parameters. To change which simulation config is used you can edit the batch_run_hom.sh script.You can also change when the tone and shock are present by changing things in the build_inputs.py script.Finally you can change how long each simulation is ran for by changing tstop in each config.
| config      | run |
| ----------- | ----------- |
| simulation_configECP_base_homogenous.json      | Baseline |
| simulation_configECP_trials_homogenous.json   | tone trials        |
| simulation_configECP_tone+shock_homogenous.json   | tone+shock conditioning        |


## To build the network
```
python build_network.py homogenous
```

## To build inputs
```
python build_input.py
```

## To run the model
```
sbatch batch_run_hom.sh
```

## To check the convergence of each cell and generate a csv called connection table
```
python connection_table
```


# The next scripts are used to plot what is going on in the network. Each simulation config has a different name for the output folder it generates. When using the scripts make sure to change the output folder to be the simulation you want to plot.

## To plot a raster 
```
python plot_raster.py
```

## To plot a firing rate histogram
```
python plot_firing_rate_distro.py
```


