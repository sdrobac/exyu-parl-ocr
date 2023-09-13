#!/bin/bash
#SBATCH -J ocr09
#SBATCH -o log-%A_%j
#SBATCH -e log-%A_%j
#SBATCH --account=Project_2002776
#SBATCH --mem=2G
#SBATCH -p small
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH -t 1-00:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=senka.drobac@gmail.com


export OMP_NUM_THREADS=4
export OMP_THREAD_LIMIT=4


dir=/scratch/project_2004614/senka-slo/data-images/1935/1935_1_3_narodnaskupština_4/

mkdir $dir/ocr-text

# the best is dpi 350
find $dir -maxdepth 1 -name "*.tif" | sort -n > list-files-for-ocr
# /users/drobac/.local/tesseract/bin/tesseract list-files-for-ocr-$year-$SLURM_ARRAY_TASK_ID $dir/ocr-text/PTK_"$year"_$SLURM_ARRAY_TASK_ID -l fin+swe
/projappl/project_2004614/local/bin/tesseract list-files-for-ocr $dir/ocr-text/ -l srp



# https://pypi.org/project/pytesseract/
# https://github.com/NanoNets/ocr-with-tesseract
# https://nanonets.com/blog/ocr-with-tesseract/#ocrwithpytesseractandopencv