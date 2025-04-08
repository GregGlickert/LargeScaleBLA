#!/bin/bash

#SBATCH --partition shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --account=umc113
#SBATCH --job-name=MAIN
#SBATCH --mem=1G
#SBATCH --output=start_blocks_expanse.out
#SBATCH --time 0-05:00

#python run_blocks_seedSweep.py
#python run_blocks_10_net.py
#python run_blocks_once.py