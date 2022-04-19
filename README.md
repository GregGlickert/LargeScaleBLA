# Amydala Fear conditioning project
### By Greg Glickert with the core stucture of the model being done by Tyler Banks

##Running the model
1) The first step is building the model
```
python build_network.py
```
2) Second compile the mod files
```
cd components/mechanisms
nrnivmodl modfiles
cd ..
cd .. 
```
3) Third run the model
```
mpirun -n 60 nrniv -mpi -python run_network.py simulation_config_base_ECP.json
```

##Analysing The model
To generate cell firing rate graphs
```
python firing_rate_breakdown.py
```
To generate a raster
```
python plot_raster.py
```
To view LFP
```
python lfp_analysis.py
```
To generate a table with connection info
```
python connection_table.py
```
Using BMTools to generate graphs
```
bmtool plot connection --sources BLA --targets BLA --sids pop_name --tids pop_name --no-prepend-pop --title 'Amydgala average convergence' convergence
```

####Env used
bmtk==0.0.9
neruon==8.0.0