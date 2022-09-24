#!/bin/bash

#SBATCH --partition compute
#SBATCH --nodes=3
#SBATCH --ntasks-per-node=120
#SBATCH --account=umc113
#SBATCH --job-name=run
#SBATCH --output=run.out
#SBATCH --mem=240G
#SBATCH --time 0-0:20

module purge
module load slurm
module load cpu
module load gcc
module load openmpi
module load ncurses

rm -rf output

echo "Running model at $(date)"

mpirun nrniv -mpi -python run_network.py simulation_config_base_ECP.json

echo "Done running model at $(date)"
