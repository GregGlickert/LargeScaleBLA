#!/bin/bash

#SBATCH -N 1
#SBATCH -n 60
#SBATCH --qos=normal
#SBATCH --job-name=amygdala_ts
#SBATCH --output=run.out
#SBATCH --time 0-12:00

START=$(date)
mpiexec nrniv -mpi -quiet -python run_network.py simulation_config_base_ECP.json
END=$(date)

echo "Done running model at $(date)"
