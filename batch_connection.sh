#!/bin/bash

#SBATCH -N 1
#SBATCH -n 1
#SBATCH --qos=normal
#SBATCH --job-name=conn_info
#SBATCH --output=conn_info.out
#SBATCH --time 0-2400:00

START=$(date)
python connection_table.py
END=$(date)

echo "Done running build at $(date)"