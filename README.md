# Large Scale model of the BLA 

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

## There are many different simulation configs that will change how the simulation is run and what is recorded. The 3 different simulatuions are baseline, tone_trials, and tone + shock trials. Each simulation can be ran by changing which config is being used when running the model in the batch_run_hom.sh file. There is also NMDA block which can be turned on and off in the json files found in the compoents/synaptic_model folder
