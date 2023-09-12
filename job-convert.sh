#!/bin/bash
#SBATCH -J conv09
#SBATCH -o log-%j
#SBATCH --account=Project_2002776
#SBATCH --mem=2G
#SBATCH -p small
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH -t 1-00:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=senka.drobac@gmail.com


# change year and PTK-19X0s in dir!!!!!
year=1909
dir=/scratch/project_2002776/data/PTK-1900s/PTK_$year  # <- change decade!

module load imagemagick/7.1.0-49

mogrify -format png   /scratch/project_2004614/senka-slo/data-images/1919/1919_3_22_PrivremenoNarodnoPredstavništvo_5/*tif
# imgDir=$dir/images

# echo $year
# echo $dir

# cd $dir
# pwd

# # rm *png
# # the best is dpi 350
# pdftopng -r 350 $dir/pdfs/PTK_"$year"_$SLURM_ARRAY_TASK_ID.pdf PTK_"$year"_$SLURM_ARRAY_TASK_ID





# mkdir $imgDir
# mkdir $imgDir/images-$SLURM_ARRAY_TASK_ID
# mv PTK_"$year"_$SLURM_ARRAY_TASK_ID*png $imgDir/images-$SLURM_ARRAY_TASK_ID

