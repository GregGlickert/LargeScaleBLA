#!/bin/bash
#SBATCH --job-name=MAIN
#SBATCH --output=start_blocks.txt
#SBATCH --time=48:00:00
#SBATCH --partition=batch
#SBATCH --nodes=1
#SBATCH --ntasks=1

#python run_blocks_seedSweep.py
python run_blocks_once.py