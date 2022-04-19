#!/bin/bash

#SBATCH -N 1
#SBATCH -n 60
#SBATCH --qos=normal
#SBATCH --job-name=amygdala_ts
#SBATCH --output=amygdala_batch.out
#SBATCH --time 0-12:00

START=$(date)
mpiexec nrniv -mpi -quiet -python run_network.py simulation_config_base.json
END=$(date)

echo "Done running model at $(date)"
