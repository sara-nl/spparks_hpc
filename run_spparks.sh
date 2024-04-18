#!/bin/bash
#SBATCH --job-name=tmp_spparks            # Job name
#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --time=1-00:00:00               # Time limit gg-hrs:min:sec
#SBATCH --array=1-10
#SBATCH --partition=rome

### Load relevant modules
module purge
module load 2022 Python/3.10.4-GCCcore-11.3.0
module load spparks/16Jan23-foss-2022a

### Define directory containing the config files 
SPPARKS="${HOME}/spparks/2024-04-17_16-42-57_5965225" # Put your own folder containing the config files
OUTPUT="${SPPARKS}"
PERSONALSPACE= "/setup/your/personal"

### Define working directory: should be scratch memory
WORKDIR="${TMPDIR}/experiment_${SLURM_ARRAY_TASK_ID}"
mkdir -p "${WORKDIR}"

### Copy relevant files to scratch - make sure to have all required files!
cp "${SPPARKS}/IN100_3d.init" "${WORKDIR}"
cp "${SPPARKS}/in.potts_am_IN100_3d" "${WORKDIR}"
cp "${OUTPUT}/config_file_${SLURM_ARRAY_TASK_ID}" "${WORKDIR}"
cp "${OUTPUT}/config_inpotts.py" "${WORKDIR}"

echo "relevant files copied to ${WORKDIR}"

cd "${WORKDIR}"

chunked_config_file="${WORKDIR}/config_file_${SLURM_ARRAY_TASK_ID}"

while IFS= read -r line; do
    case_name="$(echo -e "${line}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
    
    # This command will copy the parameter configuration to the spparks input script
    python config_inpotts.py --working_dir "${WORKDIR}" --case_name "${case_name}"

    # execute spparks for given configuration
    echo "Processing: ${case_name}/in.potts_am_IN100_3d"
    mpirun -np ${SLURM_NTASKS} spk_mpi -echo log < ${WORKDIR}/${case_name}/in.potts_am_IN100_3d
    
done < "${chunked_config_file}"

# compress everything into zip -> the all content of  ${TMPDIR}/${case_name} should be compressed 
GZIP=-9 tar -czf "${TMPDIR}/experiment_${SLURM_ARRAY_TASK_ID}.tar.gz" --exclude=*/IN100_3d.am ${WORKDIR}/vHpdV_*

# copy back to output dir
cp "${TMPDIR}/experiment_${SLURM_ARRAY_TASK_ID}.tar.gz" "${PERSONALSPACE}"