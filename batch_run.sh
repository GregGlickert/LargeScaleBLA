#!/bin/bash

#SBATCH -N 1
#SBATCH -n 60
#SBATCH --qos=normal
#SBATCH --job-name=amygdala_ts
#SBATCH --output=amygdala_batch.out
#SBATCH --time 0-12:00

START=$(date)
mpiexec nrniv -mpi -quiet -python run_network.py simulation_configECP_base.json
END=$(date)

{ printf "Start: $START \nEnd:   $END\n" }| mail -r gregglickert@mail.missouri.edu -s "Amygdala Simulation Results" -a outputECP/spikes.h5 gregglickert@mail.missouri.edu

echo "Done running model at $(date)"
