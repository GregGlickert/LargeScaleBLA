#!/bin/bash

#SBATCH -N 1
#SBATCH -n 1
#SBATCH --qos=normal
#SBATCH --job-name=building
#SBATCH --output=build.out
#SBATCH --time 0-48:00

START=$(date)
python build_network.py homogenous
END=$(date)

echo "Done running build at $(date)"
