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


{ printf "Start: $START \nEnd:   $END\n"; }| mail -r gjgpb9@mail.missouri.edu -s "Amygdala Build Complete" gjgpb9@mail.missouri.edu

echo "Done running build at $(date)"
