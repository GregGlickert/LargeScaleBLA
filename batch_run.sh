#!/bin/bash

#SBATCH -N 1
#SBATCH -n 120
#SBATCH --qos=normal
#SBATCH --job-name=amygdala
#SBATCH --output=run.out
#SBATCH --time 0-12:30

START=$(date)
#mpiexec ./components/mechanisms/x86_64/special -mpi run_network.py simulation_config_spikes_only.json
mpiexec nrniv -mpi -python run_network.py simulation_config_spikes_only.json

echo "Done running model at $(date)"
