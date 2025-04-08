#!/bin/sh
#SBATCH -J  BLA_build
#SBATCH -o  BLA_build.out
#SBATCH -e  BLA_build.error
#SBATCH -t 0-48:00:00  # days-hours:minutes

#SBATCH -N 1
#SBATCH -n 1 # used for MPI codes, otherwise leave at '1'
##SBATCH --ntasks-per-node=1  # don't trust SLURM to divide the cores evenly
##SBATCH --cpus-per-task=1  # cores per task; set to one if using MPI
##SBATCH --exclusive  # using MPI with 90+% of the cores you should go exclusive
#SBATCH --mem-per-cpu=16G  # memory per core; default is 1GB/core

## send mail to this address, alert at start, end and abortion of execution
##SBATCH --mail-type=ALL
##SBATCH --mail-user=EMAILHERE

START=$(date)
echo "Started running at $START."

unset DISPLAY
python build_network.py homogenous

END=$(date)
echo "Done running simulation at $END"
