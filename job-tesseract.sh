#!/bin/bash
#SBATCH -J ocr09
#SBATCH -o log-%j
#SBATCH -e log-%j
#SBATCH --account=Project_2002776
#SBATCH --mem=2G
#SBATCH -p small
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH -t 3-00:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=senka.drobac@gmail.com


export OMP_NUM_THREADS=4
export OMP_THREAD_LIMIT=4


# dir=/scratch/project_2004614/senka-slo/data-images/1935/1935_1_3_narodnaskupština_4/


for dir in $(find /scratch/project_2004614/senka-slo/data-images/ -mindepth 2 -maxdepth 2); do
    cd $dir
    find $dir -maxdepth 1 -name "*.tif" | sort -n > list-files-for-ocr
    /projappl/project_2004614/local/bin/tesseract list-files-for-ocr ocr-tesseract -l srp -c preserve_interword_spaces=1 -c page_separator="[PAGE_BREAK]"
done

# dir=/scratch/project_2004614/senka-slo/data-images/1935/1935_1_3_narodnaskupština_4/
# cd $dir
# find $dir -maxdepth 1 -name "*.tif" | sort -n > list-files-for-ocr
# /projappl/project_2004614/local/bin/tesseract list-files-for-ocr ocr-tesseract -l srp -c preserve_interword_spaces=1 -c page_separator="-------------------------------------[PAGE_BREAK]"



# https://pypi.org/project/pytesseract/
# https://github.com/NanoNets/ocr-with-tesseract
# https://nanonets.com/blog/ocr-with-tesseract/#ocrwithpytesseractandopencv