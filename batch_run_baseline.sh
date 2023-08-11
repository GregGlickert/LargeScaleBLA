#!/bin/bash

#SBATCH -N 1
#SBATCH -n 50
#SBATCH --mem-per-cpu=2G
#SBATCH --qos=normal
#SBATCH --job-name=amygdala_theta
#SBATCH --output=amygdala_baseline.out
#SBATCH --time 0-12:00

START=$(date)
mpiexec nrniv -mpi -quiet -python run_network.py simulation_configECP_baseline_homogenous.json
END=$(date)

echo "Done running model at $(date)"
