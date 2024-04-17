#!/bin/bash
#SBATCH --job-name=gen_config            # Job name
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=128
#SBATCH --time=00:30:00               # Time limit hrs:min:sec
#SBATCH --partition=rome

SPPARKS="${HOME}/spparks"
OUTPUT="${SPPARKS}/$(date +%Y-%m-%d_%H-%M-%S)_${SLURM_JOBID}"
mkdir -p $OUTPUT

# Activate environment and load necessary modules
source ../venv/bin/activate
module load 2022 
module load Python/3.10.4-GCCcore-11.3.0

cd ./config

# copy relevant files 
cp param_space.yaml "$TMPDIR"

python config_file_gen.py --yaml_file "$TMPDIR"/param_space.yaml --output_dir "$TMPDIR"

cp "$TMPDIR"/param_space.yaml $OUTPUT
cp -r "$TMPDIR"/config_file_* $OUTPUT