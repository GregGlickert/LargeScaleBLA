#!/bin/bash

#SBATCH -N 1
#SBATCH -n 50
#SBATCH --qos=normal
#SBATCH --job-name=BLA
#SBATCH --output=BLA.out
#SBATCH --time 0-12:00

START=$(date)
mpiexec nrniv -mpi -quiet -python run_network.py simulation_config.json
END=$(date)

{ printf "Start: $START \nEnd:   $END\n" & python analysis.py --save-plots & printf "\n\n" & git diff components/synaptic_models/; }| mail -r gregglickert@mail.missouri.edu -s "Large Scale BLA Results" -a analysis.png gregglickert@mail.missouri.edu

echo "Done running model at $(date)"
