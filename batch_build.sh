#!/bin/bash

#SBATCH -N 1
#SBATCH -n 1
#SBATCH --qos=normal
#SBATCH --job-name=amygdala_build
#SBATCH --output=amygdala.out
#SBATCH --time 0-2400:00

START=$(date)
python build_network.py
END=$(date)

echo "Done running build at $(date)"
