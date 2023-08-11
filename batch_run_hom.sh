#!/bin/bash

#SBATCH -N 1
#SBATCH -n 100
#SBATCH --mem-per-cpu=2G
#SBATCH --qos=normal
#SBATCH --job-name=amygdala
#SBATCH --output=amygdala_batch1.out
#SBATCH --time 0-23:00

START=$(date)
mpiexec nrniv -mpi -quiet -python run_network.py simulation_configECP_tone+shock_homogenous.json
END=$(date)

echo "Done running model at $(date)"
