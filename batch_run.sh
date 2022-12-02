#!/bin/bash

#SBATCH -N 1
#SBATCH -n 90
#SBATCH --qos=normal
#SBATCH --job-name=amygdala
#SBATCH --output=run.out
#SBATCH --time 0-12:30



START=$(date)
mpiexec nrniv -mpi -quiet -python run_network.py simulation_config_spikes_only.json
END=$(date)

echo "Done running model at $(date)"
