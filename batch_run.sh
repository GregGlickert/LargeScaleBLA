#!/bin/bash

#SBATCH -N 1
#SBATCH -n 100
#SBATCH --qos=normal
#SBATCH --job-name=amygdala
#SBATCH --output=run.out
#SBATCH --time 0-12:30

export HDF5_USE_FILE_LOCKING=FALSE

#export PYTHONPATH=$HOME/install/lib/python:$PYTHONPATH
#export PATH=$HOME/install/bin:$PATH

export PYTHONPATH=$HOME/install-cpu/lib/python:$PYTHONPATH
export PATH=$HOME/install-cpu/bin:$PATH


START=$(date)
#./components/mechanisms/x86_64/special 
mpiexec ./components/mechanisms/x86_64/special -mpi run_network.py simulation_config_spikes_only.json
#python run_network.py
END=$(date)

echo "Done running model at $(date)"
#mpirun ./components/mechanisms/x86_64/special -python -mpi -gpu run_network.py simulation_config_spikes_only.json

#mpirun -n 2 ./components/mechanisms/x86_64/special -mpi -c coreneuron=1 -c gpu=1 run_network.py simulation_config_spikes_only.json --cell-permute 2

#mpirun -n 1 nrniv-core --mpi --gpu --cell-permute 2 --python run_network simulation_config_spikes_only.json

#mpiexec nrniv -mpi -quiet -python run_network.py simulation_config_spikes_only.json