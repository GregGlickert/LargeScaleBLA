#!/bin/bash

#SBATCH -N 1
#SBATCH -n 140
#SBATCH --qos=normal
#SBATCH --job-name=amygdala_theta
#SBATCH --output=amygdala_batch.out
#SBATCH --time 0-12:00

START=$(date)
mpiexec nrniv -mpi -quiet -python run_network.py simulation_configECP_base_homogenous.json
END=$(date)

echo "Done running model at $(date)"
