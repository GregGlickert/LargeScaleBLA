#!/bin/bash

#SBATCH -N 1
#SBATCH -n 1
#SBATCH --qos=normal
#SBATCH --job-name=amygdala_build
#SBATCH --output=build3.out
#SBATCH --time 0-2400:00

START=$(date)
python plot_LTD_vs_Firing.py
END=$(date)

echo "Done running build at $(date)"
