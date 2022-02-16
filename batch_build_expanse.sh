#!/bin/bash

#SBATCH --partition shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --account=umc113
#SBATCH --job-name=build_BLA
#SBATCH --mem=8G
#SBATCH --output=build.out
#SBATCH --time 0-02:00

module purge
module load slurm
module load cpu
module load intel
module load intel-mpi
module load ncurses

echo "Building model at $(date)"

python build_network.py

echo "Done building model at $(date)"